from common.util.fp import File
import sys
INPUT_EXCEL_DIR='data/xx/12_26'
OUT_PUT_DIR='data/xx/gen'
class ExcelUtil:
    
    def test(self):
        print("test")

    def e_to_t(self):
        for f in File(INPUT_EXCEL_DIR).list_dir():
            File(f'{OUT_PUT_DIR}/{f.name}.json').write_file(f.dump())
            print(f.path)
            break
    
    def dont_happy_12_26(self):
        path=f'{OUT_PUT_DIR}/11月收支表新(1).json'
        src=File(path).read_file()
        s1,s3=src['Sheet1'],src['Sheet3']
        s=dict()
        for name,value in s3['联系电话'].items():
            s[value]=s3["客户姓名"][name]
        for name,value in s1['联系方式'].items():
            kh_name=s1['客户姓名'][name]
            #if str(kh_name) == 'nan':
            print(f"{value},{kh_name},{s.get(value)}")
            

if __name__=="__main__":
    getattr(ExcelUtil(),sys.argv[1])(*sys.argv[2:])
