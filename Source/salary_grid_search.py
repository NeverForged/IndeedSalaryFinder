import sys
import time
import string
import random
import requests
import html.parser
from bs4 import BeautifulSoup

class IndeedSalaryFinder(object):
    '''
    Scrapes Indeed to find the Salary associated with the job in question.
    '''

    def __init__(self, query):
        '''
        query - a query to find the job, better queries are better
        '''
        self.query = query

    def find(self, job_id, city='Seattle', state='WA'):
        '''
        Actual scrape function
        '''
        self.no = []
        self.yes = []
        salary = 100
        go = 'yes'
        while go == 'yes':
            new = int(salary/2)
            if new == 0:
                new = 1
            time.sleep(random.randint(0,1))
            if salary <= 25:
                # poverty level...
                go = 'no'
            n = self.get_search(salary, job_id, city, state)
            # print(salary, n)
            if n >= 0:
                try:
                    self.yes.index(salary)
                    go = 'no'
                except:
                    self.yes.append(salary)
                    if len(self.no) >= 1:
                        new = int((min(self.no) - salary)/2)
                    if new <= 0:
                        new = 1
                    salary = salary + new
            else:
                try:
                    self.no.index(salary)
                    go = 'no'
                except:
                    self.no.append(salary)
                    if len(self.yes) >= 1:
                        new = int((salary - max(self.yes))/2)
                    if new <= 0:
                        new = 1
                    salary = salary - new
        print('{}K to {}k by Indeed'.format(max(self.yes), min(self.no)))

    def get_search(self, salary, job_id, city='Seattle', state='WA'):
        '''
        Searches for the job in Indeed... using the search function,
        finds the job_id in the html, or not.
        '''
        r = requests.get('https://www.indeed.com/jobs?q=' + self.query + '+' +
                         '%24' + str(salary) + '%2C000&l=' + city + '%2C+' +
                         state)
        soup = BeautifulSoup(r.content, 'html.parser')
        tags  = soup.find_all()
        return str(tags).find(job_id)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Type in a query, such as: "data+science+galvanize" and ')
        print('the job_id.')
        print()
        print('job_id -> Make sure the search reveals 2-10 jobs.' )
        print('view source')
        print('find: jobmap')
        print('grab the long string after rd for your job.')
    else:
        finder = IndeedSalaryFinder(sys.argv[1])
        finder.find(sys.argv[2])
