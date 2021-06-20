# simulation with no cost constraint

from util import getdata
from mcitr import MCITR
import numpy as np
from multiprocessing import Pool
from functools import partial


def run(seed, sample_size, case):

    Y_train, X_train, A_train, optA_train = getdata(sample_size, case=case, seed=seed)
    Y_test, X_test, A_test, optA_test = getdata(2000, case=case, seed=seed + 200)

    mcitr = MCITR()
    history = mcitr.fit(Y_train, X_train, A_train, device="cpu", verbose=0, epochs=200)

    D_test = mcitr.predict(X_test, A_test)

    accuracy, value = mcitr.evaluate(Y_test, A_test, D_test, X_test, optA_test)

    return accuracy, value
    

def main():

    sample_size_list = [200, 400, 800, 2000] # training sample size
    case_list = np.arange(1, 9) # data generation cases
    seed_list = np.arange(200) # 200 replicate for each simulation setting

    # unconstrained simulation 

    accuracy_list = np.zeros((4, 8, 200))
    value_list = np.zeros((4, 8, 200))

    for iss, sample_size in enumerate(sample_size_list):

        print("---- sample size: {0} ----".format(sample_size))

        for ic, case in enumerate(case_list):

            print("---- case number: {0} ----".format(case))

            with Pool(8) as p:
                run_part = partial(run, sample_size=sample_size, case=case)
                accuracy_ls, value_ls = zip(*p.map(run_part, seed_list))

            accuracy_list[iss, ic, :] = accuracy_ls
            value_list[iss, ic, :] = value_ls

            np.save("accuracy_uncstr_parallel", accuracy_list)
            np.save("value_uncstr_parallel", value_list)


if __name__ == "__main__":
    
    main()

