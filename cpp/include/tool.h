#include <stdio.h>
FILE *LOG_FILE = fopen("data/context/loj_p2885/case1/c.log","w");
void log(const char *format, ...) {
    char s[2048];
    va_list args;
    
    va_start(args, format);
    
    // 使用 vsnprintf 防止缓冲区溢出
    int len = vsnprintf(s, sizeof(s), format, args);
    
    va_end(args);
    
    if (len > 0) {
        // 使用 fwrite 写入实际长度
        fwrite(s, 1, len, LOG_FILE);
        // 或者更简单的方式：
        // fputs(s, LOG_FILE);
    }
    
    fflush(LOG_FILE);
}