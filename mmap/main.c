#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>

int main()
{
    printf("[TEST]: Start\n");

    int fd = open("/dev/mem", O_RDWR | O_SYNC);
    unsigned long addr = 0xE000A000;
    unsigned long size = 0x000000FC;
    void* base = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, addr);

    for (size_t i = 0; i < size; i += 4)
    {
        printf("[MMAP]: 0x%08lX: 0x%08lX\n", addr + i, *(volatile unsigned long*)(base + i));
    }

    printf("[TEST]: Finish\n");
    return 0;
}
