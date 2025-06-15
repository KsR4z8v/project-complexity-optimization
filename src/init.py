from generate_minizinc_model import GenerateMinizincCode
from view import View

def main():
  generateModelMinizinc = GenerateMinizincCode()
  View(generateModelMinizinc)

if(__name__ == '__main__'):
  main()
