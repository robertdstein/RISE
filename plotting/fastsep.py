import argparse
parser = argparse.ArgumentParser()
parser.add_argument("decay")
args = parser.parse_args()

filename = "separation" + args.decay + ".py"

print filename

execfile(filename)