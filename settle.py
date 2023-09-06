import numpy as np
import logging
# import argparse
import os
import csv


names = {'donghee', 'choongwon'}
dates = {'2023-09-01','2023-09-02','2023-09-03'}
whos = {'share', 'donghee', 'choongwon'}

class Settle():
    def __init__(self, person):
        self.person = person
        self.account = {
            'dates': list(),
            'contents': list(),
            'amounts': list(),
            'whos': list(),
        }

    def __getitem__(self, k):
        if k in self.account:
            return self.account[k]
        else:
            raise KeyError(f"{k} not found in account.")
    
    def __len__(self):
        return len(self.account['dates'])
    
    def when2content(self, date):
        pass

    def add_entry(self, entry):
        self.account['dates'].append(entry[0])
        self.account['contents'].append(entry[1])
        self.account['amounts'].append(int(entry[2]))
        self.account['whos'].append(entry[3])
    
    def end_entry(self):
        for k, v in self.account.items():
            self.account[k] = np.array(v)
    
    def log(self):
        for i in range(len(self)):
            sen = ''
            for k in self.account.keys():
                sen += str(self.account[k][i]) + ' '
            logging.info(f'{self.person}: {sen}')

    def read_csv(self, csv_path):
        with open(csv_path, 'r') as f:
            csv_reader = csv.reader(f)
            for entry in csv_reader:
                entry = sanity_check(entry)
                self.add_entry(entry)
                
        return True
    
    def pre_cal(self):
        for k, v in self.account.items():
            self.account[k] = np.array(v)
        
        self.pay = np.sum(self.account['amounts'])
        self.owe = dict()
        for name in names:
            self.owe[name] = np.sum(self.account['amounts'][np.where(self.account['whos']==name)])
        self.owe['share'] = np.sum(self.account['amounts'][np.where(self.account['whos']=='share')])


def sanity_check(entry):
    # if len(entry) != 4:
    #     print('Wrong format. len should be 4')
    #     return False
    # if entry[0] not in dates:
    #     print("Wrong date. should be {1,2,3}")
    #     return False
    # # if type(entry[1]) != str:
    # #     print("Wrong content. Should be str")
    # #     return False
    # if type(int(entry[2])) != int:
    #     print("Wrong amount. Should be string")
    #     return False
    # if type(entry[3]) != int:
    #     print("Wrong amounts. Should be int")
    #     return False
    # if len(entry) == 4:
    #     entry[4] = 'share'
    # elif type(entry[4]) not in whos:
    #     print("Wrong whos. Should be {'share', 'donghee', 'andrew'}")
    #     return False

    assert len(entry) == 4, 'wrong format. len should be 4'
    assert entry[0] in dates, 'wrong date. should be in {1,2,3}'
    assert int(entry[2]), 'wrong amount. should be int'
    assert entry[3] in whos, 'wrong whos. should be in {share, donghee, choongwon}'
    # try:
    #     entry = {
    #         'dates': entry[0],
    #         'contents': entry[1],
    #         'amounts': int(entry[2]),
    #         'whos': entry[3],
    #         }
    #     return entry
    # except:
    #     logging.info("Wrong format")
    #     return False
    return entry

# def parse_args():
#     parser = argparse.ArgumentParser(description="Settle")
#     parser.add_argument("--csv-path", required=True, help="path to CSV file.")
#     args = parser.parse_args()

#     return args

def calculate(settles):
    pays = {
        'donghee': 0,
        'choongwon': 0,
    }
    owes = {
        'donghee': 0,
        'choongwon': 0,
        'share': 0,
    }
    for name in names:
        pays[name] += settles[name].pay
        for name_again in names:
            owes[name] += settles[name_again].owe[name]
        owes['share'] += settles[name].owe['share']
    
    donghee_should_pay = owes['share']*0.5 + owes['donghee'] - pays['donghee'] ## +: owe
    choongwon_should_pay = owes['share']*0.5 + owes['choongwon'] - pays['choongwon']
    share = owes['share']

    logging.info('====================')
    # logging.info('minus(-): owe, plus(+): overpay')
    # logging.info(f'Donghee should pay: {donghee_should_pay}')
    # logging.info(f'Choongwon should pay: {choongwon_should_pay}')

    if donghee_should_pay > choongwon_should_pay:
        logging.info(f"* Donghee should pay {donghee_should_pay}")
    else:
        logging.info(f"* Choongwon should pay {choongwon_should_pay}")

    logging.info("======= Done ======")


## name.csv / date,content,amount,whos
def main():
    logging.basicConfig(filename='settle.txt', level=logging.INFO)

    basepath = os.path.dirname(__file__)
    settles = {}
    for name in names:
        settles[name] = Settle(name)
        p = os.path.join(basepath, name + '.csv')
        settles[name].read_csv(p)
        settles[name].log()
        settles[name].pre_cal()

    calculate(settles)

    


    
    # entry = True 
    # while entry is True:
    #     entry = input("input the event in this format: Person/Date(1,2,3)/Contents/Amounts(int)/Whos(share(default), donghee, choongwon)")
    #     try:
    #         entry = entry.split('/')
    #     except:
    #         logging.info("Wrong format")
    #         continue

    #     entry = sanity_check(entry)

    #     if not entry:
    #         continue
    #     else:
    #         name = entry[0]
        
    #     settles[name].add_entry(entry)
    
    # for name in names:
    #     settles[name].end_entry()
    #     settles[name].log()
    


if __name__ == '__main__':
    main()

    ## date content amount
