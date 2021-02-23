import xlrd
import uuid
import json
from string import ascii_uppercase
from pprint import pprint
from datetime import datetime
from db_provider import db_provider as db
from service_config import DIRS
from client import client

SIZES = (0, 1, 2, 4)

class ServiceErrors(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
        
class Service:
    def __init__(self, *, db):
        self.db = db
        raw_scheme = client.scheme
        if raw_scheme:
            scheme = self.make_scheme(raw_scheme)
            db.add_scheme(scheme)
        else:
            pass

    def _define_position_size(self, size):
        if sum(map(lambda x: x > 2000, size)):
            return 0
        check = sum(map(lambda x: x <= 1000, size))
        if check == 3:
            return 1
        elif check == 2:
            return 2
        else:
            return 4

    def add_packing_list(self, data):
        file_name = f'{DIRS.get("upload")}/table_recieved_{str(datetime.now())}.xls'
        try:
            with open(file_name, 'wb') as fd:
                fd.write(data)
        except (FileNotFoundError, TypeError):
            raise ServiceErrors('file does not save')
        parser = Parser(file_name).get_item_list()
        return self._calculate(parser)

    def get_warehouse_list(self):
        warehouse_list = db.get_warehouse_list()
        return [{'name': x[1], 'id': x[0]} for x in warehouse_list]

    def make_scheme(self, raw_scheme):
        size_x = raw_scheme.get('size').get('size_x')
        size_y = raw_scheme.get('size').get('size_y')
        scheme  = []
        warehouse = []
        for number in range(1, size_y + 1):
            for letter in ascii_uppercase[:size_x]:
                scheme.append([letter + str(number),  [letter + str(number)]])
        for position in scheme:
            for merge in raw_scheme.get('merged'):
                if list(position)[0] in merge:
                    position[1] = merge
        for position in scheme:
            if not position[1]:
                warehouse.append([position[0],])
            elif position[1] in warehouse:
                pass
            else:
                warehouse.append(position[1])
        db.add_warehouse(warehouse)
        return scheme

    def _calculate(self, packing_list):
        to_send = []
        """Удаление очень больших позиций и отправка из на удаленный склад"""
        c = 0
        for item in packing_list:
            if self._define_position_size(item.get('size')) == 0:
                db.add_item_to_remote(item)

        items_by_size = {x: [] for x in SIZES} #Словарь с индексом - размером позиций
        for item in packing_list:
            items_by_size[self._define_position_size(item.get('size'))].append(item)

        """Для больших позиций"""
        empty_positions_count = len(db.get_empty_pos_by_size(4))

        for item in items_by_size[4][empty_positions_count:]:
            db.add_item_to_remote(item)

        positions = sorted(db.get_empty_pos_by_size(4), key=lambda x: x[0][0], reverse=True)

        items = sorted(items_by_size[4][:len(db.get_empty_pos_by_size(4))], key=lambda x: x.get('weight'), reverse=True)

        for i in range(len(items)):
            position = positions[i]
            item = items[i]
            db.add_item_to_position(item, position, 4)
            to_send.append({'destination': position, 'uuid': item.get('uuid')})

        """Для средних позиций"""
        empty_positions_count = len(db.get_empty_pos_by_size(4)) + len(db.get_empty_pos_by_size(2))

        for item in items_by_size[2][empty_positions_count:]:
            db.add_item_to_remote(item)

        positions = sorted(db.get_empty_pos_by_size(2), key=lambda x: x[0][0], reverse=True)\
                + sorted(db.get_empty_pos_by_size(4), key=lambda x: x[0][0], reverse=True)

        items = sorted(items_by_size[2][:len(db.get_empty_pos_by_size(4)) + len(db.get_empty_pos_by_size(2))],
                key=lambda x: x.get('weight'),
                reverse=True)

        for i in range(len(items)):
            position = positions[i]
            item = items[i]
            db.add_item_to_position(item, position, 2)
            to_send.append({'destination': position, 'uuid': item.get('uuid')})

        """Для мелких позиций"""
        empty_positions_count = len(db.get_empty_pos_by_size(4))\
                + len(db.get_empty_pos_by_size(2))\
                + len(db.get_empty_pos_by_size(1))

        for item in items_by_size[1][empty_positions_count:]:
            db.add_item_to_remote(item)

        positions = sorted(db.get_empty_pos_by_size(1), key=lambda x: x[0][0], reverse=True)\
                + sorted(db.get_empty_pos_by_size(2), key=lambda x: x[0][0], reverse=True)\
                + sorted(db.get_empty_pos_by_size(4), key=lambda x: x[0][0], reverse=True)

        items = sorted(items_by_size[1][:len(db.get_empty_pos_by_size(4)) + len(db.get_empty_pos_by_size(2)) + len(db.get_empty_pos_by_size(1))],
                key=lambda x: x.get('weight'),
                reverse=True)

        for i in range(len(items)):
            position = positions[i]
            item = items[i]
            db.add_item_to_position(item, position, 1)
            to_send.append({'destination': position, 'uuid': item.get('uuid')})
        r = client.send_warehouse_to_api(to_send)
        return r

    def get_remote_list(self):
        return db.get_remote_list()

    def checkout(self, position):
        db.checkout(position)
        return client.checkout(position)

    def get_checkout_list(self):
        checkout_list = db.get_checkout_list()
        return [{'name': x[0], 'id': x[2]} for x in checkout_list]

class Parser:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_item_list(self):
        item_list = []
        wb = xlrd.open_workbook(self.file_name)
        sheet = wb.sheet_by_index(0)
        try:
            for i in range(1, sheet.nrows):
                size = list(map(int, sheet.row_values(i)[2].split('*')))
                item_list.append({'name': sheet.row_values(i)[1],
                    'weight': float(sheet.row_values(i)[3]),
                    'size': size,
                    'uuid': str(uuid.uuid4())})
        except (ValueError, IndexError):
            raise ServiceErrors('file does not read')
        return item_list

service = Service(db=db)
