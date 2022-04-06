#include "xparameters.h"
#include "xil_types.h"
#include "xil_io.h"

#define MAILBOX_CMD_ADDR (*(volatile unsigned *)(0x0000FFFC))
#define MAILBOX_ADDR (*(volatile unsigned *)(0x0000FFF8))
#define MAILBOX_DATA(x) (*(volatile unsigned *)(0x0000FF00+((x)*4)))

int main (void) {
    int cmd, count, i;
    while(1){
        while((MAILBOX_CMD_ADDR & 0x01)==0);
        cmd=MAILBOX_CMD_ADDR;

        count = (cmd & 0x0000ff00) >> 8;
        if((count==0) || (count>253)) {
            // clear bit[0] to indicate cmd processed,
            // set rest to 1s to indicate error in cmd word
            MAILBOX_CMD_ADDR = 0xfffffffe;
            return -1;
        }
        for(i=0; i<count; i++) {
            if (cmd & 0x08) // Python issues read
            {
                switch ((cmd & 0x06) >> 1) { // use bit[2:1]
                    case 0 : MAILBOX_DATA(i) = *(u8 *) MAILBOX_ADDR; break;
                    case 1 : MAILBOX_DATA(i) = *(u16 *) MAILBOX_ADDR; break;
                    case 2 : break;
                    case 3 : MAILBOX_DATA(i) = *(u32 *) MAILBOX_ADDR; break;
                }
            }
            else // Python issues write
            {
                switch ((cmd & 0x06) >> 1) { // use bit[2:1]
                case 0 : *(u8 *)MAILBOX_ADDR = (u8 *) MAILBOX_DATA(i); break;
                case 1 : *(u16 *)MAILBOX_ADDR = (u16 *) MAILBOX_DATA(i); break;
                case 2 : break;
                case 3 : *(u32 *)MAILBOX_ADDR = (u32 *)MAILBOX_DATA(i); break;
                }
            }
        }
        MAILBOX_CMD_ADDR = 0x0;
    }
    return 0;
}
