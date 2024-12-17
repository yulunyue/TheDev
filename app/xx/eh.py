from common.util.fp import File
import sys
INPUT_EXCEL_DIR='data/xx/kd'
OUT_PUT_DIR='data/xx/gen'
class ExcelUtil:
    
    def test(self):
        print("test")

    def e_to_t(self):
        for f in File(INPUT_EXCEL_DIR).list_dir():
            File(f'{OUT_PUT_DIR}/{f.name}.json').write_file(f.dump())
            print(f.path)
            break
            


if __name__=="__main__":
    getattr(ExcelUtil(),sys.argv[1])(*sys.argv[2:])
