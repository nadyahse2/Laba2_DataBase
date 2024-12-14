import csv
import os
from datetime import date
import openpyxl
def update_index_with_offsets(file,file_ind,field_index):
    if os.path.exists(file):
        if os.path.exists(file_ind):
            os.remove(file_ind)
        key_offsets = {}
        l = []
        with open(file,'r',newline='',encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            offset = count_bytes(header)
            for row in reader:

                key = row[field_index]
                l.append(row[field_index])
                key_offsets.setdefault(key, []).append(offset)
                offset += count_bytes(row)



        with open(file_ind, 'a', newline='',encoding='utf-8') as f_ind:
            writer = csv.writer(f_ind)
            for key, offsets in key_offsets.items():
                writer.writerow([key] + offsets)
        return l




def count_bytes(lis):
    header_bytes = 0
    delimiter_bytes = len(','.encode('utf-8'))

    for i, item in enumerate(lis):
        header_bytes += len(item.encode('utf-8'))
        if i < len(lis) - 1:
            header_bytes += delimiter_bytes

    return header_bytes + len('\n'.encode('utf-8'))






class TravelManager:
    def __init__(self):
        self.file = 'travel_journal.csv'
        self.fields = ['trip_id','destination','start_date','end_date','transport']
        self.var = {1:[],2:[],3:[],4:[]}
        if not os.path.exists(self.file):
            with open(self.file,'w',newline='',encoding='utf-8') as db:
                writer = csv.writer(db)
                writer.writerow(self.fields)
            with open(self.file,'r',newline='',encoding='utf-8') as db:
                for l in db:
                    self.len_title = len(l)


    #def open_db(self):
    def delete_db(self):
        #if os.path.exists(self.file):
            os.remove(self.file)
    def clean_db(self):
        #if os.path.exists(self.file):
            os.truncate(self.file ,self.len_title)

    def save_db(self):
        os.replace(self.file + '.tmp', self.file)
        self.var[1] = list(set(update_index_with_offsets(self.file, 'description.csv', 1)))
        self.var[2] = list(set(update_index_with_offsets(self.file, 'start_date.csv', 2)))
        self.var[3] = list(set(update_index_with_offsets(self.file, 'end_date.csv', 3)))
        self.var[4] = list(set(update_index_with_offsets(self.file, 'transport.csv', 4)))
    def add_row(self, new_record):
        insert = False
        with open(self.file, 'r', newline='',encoding='utf-8') as f, open(self.file+'.tmp', 'a',newline='',encoding='utf-8') as tmp:
            reader = csv.reader(f)
            writer = csv.writer(tmp)
            header = next(reader)
            writer.writerow(header)
            dupl = False
            for row in reader:
                if row[1] == new_record[1] and row[2] == str(new_record[2]) and row[3] == str(new_record[3]) and row[4] == new_record[4]:

                    return False, 'Row already exists'
                if new_record[0] < int(row[0]) and not insert:
                    writer.writerow(new_record)
                    insert = True
                writer.writerow(row)

                if int(row[0]) == new_record[0]:
                    dupl = True
            if dupl or not insert:
                if dupl:
                   new_record[0] = int(row[0])+1
                writer.writerow(new_record)

        return True
    def delete_row(self, field):
        with open(self.file, 'r', newline='',encoding='utf-8') as f, open(self.file + '.tmp', 'w', newline='',encoding='utf-8') as tmp:
            reader = csv.reader(f)
            writer = csv.writer(tmp)
            header = next(reader)
            writer.writerow(header)
            for row in reader:
                if not (str(field) in row):
                    writer.writerow(row)
        return True
    def search_row(self,field):
        result =[]
        if field in self.var[1]:
            with open('description.csv','r',newline='',encoding='utf-8') as d:
                reader = csv.reader(d)
                for row in reader:
                    if row[0] == field:
                        lis = row[1:]
                        lis_res = list(map(int,lis))
            with open(self.file,'r',newline='',encoding='utf-8') as db:
                for i in lis_res:
                   db.seek(i)
                   reader = csv.reader(db)
                   next(reader)
                   for row in reader:
                       result.append(row)
                       break
        elif field in self.var[2]:
            with open('start_date.csv','r',newline='',encoding='utf-8') as d:
                reader = csv.reader(d)
                for row in reader:
                    if row[0] == field:
                        lis = row[1:]
                        lis_res = list(map(int,lis))
            result = []
            with open(self.file,'r',newline='',encoding='utf-8') as db:
                for i in lis_res:
                   db.seek(i)
                   reader = csv.reader(db)
                   next(reader)
                   for row in reader:
                       result.append(row)
                       break
        elif field in self.var[3]:
            with open('end_date.csv','r',newline='',encoding='utf-8') as d:
                reader = csv.reader(d)
                for row in reader:
                    if row[0] == field:
                        lis = row[1:]
                        lis_res = list(map(int,lis))
            result = []
            with open(self.file,'r',newline='',encoding='utf-8') as db:
                for i in lis_res:
                   db.seek(i)
                   reader = csv.reader(db)
                   next(reader)
                   for row in reader:
                       result.append(row)
                       break
        elif field in self.var[4]:
            with open('transport.csv','r',newline='',encoding='utf-8') as d:
                reader = csv.reader(d)
                for row in reader:
                    if row[0] == field:
                        lis = row[1:]
                        lis_res = list(map(int,lis))
            result = []
            with open(self.file,'r',newline='',encoding='utf-8') as db:
                for i in lis_res:
                   db.seek(i)
                   reader = csv.reader(db)
                   next(reader)
                   for row in reader:
                       result.append(row)
                       break
        else:
            with open(self.file, 'r', newline='', encoding='utf-8') as db:
                reader = csv.reader(db)
                next(reader)
                for row in reader:
                    if row[0] == field:
                        result.append(row)
        return result

    def create_backup(self):
            backup_filename = "travel_journal_backup.csv"
            with open(self.file, 'r', encoding='utf-8') as source, open(backup_filename, 'w',encoding='utf-8') as dest:
                for line in source:
                    dest.write(line)
            return True
    def restore_from_backup(self):
            backup_filename = "travel_journal_backup.csv"
            if os.path.exists(backup_filename):
              os.replace(backup_filename, self.file)
              self.var[1] = list(set(update_index_with_offsets(self.file, 'description.csv', 1)))
              self.var[2] = list(set(update_index_with_offsets(self.file, 'start_date.csv', 2)))
              self.var[3] = list(set(update_index_with_offsets(self.file, 'end_date.csv', 3)))
              self.var[4] = list(set(update_index_with_offsets(self.file, 'transport.csv', 4)))
              return True, 'Good'
            else:
              return False, "Backup file not found."

    def import_from_excel(self, excel_filename="travel_journal.xlsx"):
        data = []
        with open(self.file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)

        #Create a new Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for row in data:
            sheet.append(row)
        workbook.save(excel_filename)

        return os.path.abspath(excel_filename)



if __name__ == "__main__":
    datebase = TravelManager()
