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
        self._f.write('block_num,trial_num,trial_type,offer,choice,\
                      avg_grip,success,outcome_self,outcome_other,MVC,fatigue_rating')

    def write(self, block_num, trial_num, trial_type, offer,\
               choice, avg_grip, success, outcome_self, \
                outcome_other, MVC, fatigue_rating):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%i,%s,%s,%s,%f,%i,%i,%i,%i,%i'%(
            block_num, trial_num, trial_type, offer,\
                choice, avg_grip, success, outcome_self,\
                      outcome_other, MVC, fatigue_rating)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()

class CSVWriter_trial:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d_trial_dat.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('block_num,trial_num,trial_type,offer,choice,\
                      avg_grip,success,outcome_self,outcome_other')

    def write(self, block_num, trial_num, trial_type, offer,\
               choice, avg_grip, success, outcome_self, \
                outcome_other):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%i,%s,%s,%s,%f,%i,%i,%i'%(
            block_num, trial_num, trial_type, offer,\
                choice, avg_grip, success, outcome_self,\
                      outcome_other)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()

        
class CSVWriter_block:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d_block_dat.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('block_num,fatigue_rating')

    def write(self, block_num, fatigue_rating):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%i'%(
            block_num, fatigue_rating)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()

class CSVWriter_subj:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d_subj_dat.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('subj_id,MVC')

    def write(self, subj_num, MVC):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%f'%(
            subj_num, MVC)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()