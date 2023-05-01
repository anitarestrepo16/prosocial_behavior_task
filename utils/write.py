import os

class TSVWriter:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d.tsv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('trial_num\ttrial_type\toffer\tchoice\tsuccess\toutcome_self\toutcome_other')

    def write(self, trial_num, trial_type, offer,\
               choice, success, outcome_self, outcome_other):
        '''
        writes a trial's parameters to log
        '''
        line = '\n%i\t%s\t%s\t%s\t%i\t%i\t%i'%(
            trial_num, trial_type, offer,\
                  choice, success, outcome_self, outcome_other)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()

class CSVWriter:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('trial_num,trial_type,offer,choice,success,outcome_self,outcome_other')

    def write(self, trial_num, trial_type, offer,\
               choice, success, outcome_self, outcome_other):
        '''
        writes a trial's parameters to log
        '''
        line = '\n%i,%s,%s,%s,%i,%i,%i'%(
            trial_num, trial_type, offer,\
                  choice, success, outcome_self, outcome_other)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()