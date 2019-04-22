import kenlm
from model.proofreader import CNProofReader

if __name__ == "__main__":
    pf = CNProofReader()
    while True:
        sent = input()
        print(pf.proofread(sent))