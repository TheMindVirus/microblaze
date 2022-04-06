#include "xparameters.h"
#include "xil_types.h"
#include "xil_io.h"

#define ENTRY              int main(void)
#define RETURN(X)          return X

#define IF                 if
#define ELSE               else
#define WHILE              while

#define CAST(X, T)         (T)(X)
#define FETCH(X)           *(X)

#define REGISTER_ADDRESS   0x0000FFF8
#define REGISTER_RPIDATA   0x0000FF00
#define REGISTER_COMMAND   0x0000FFFC
#define REGISTER_TYPE      volatile unsigned*

#define MEMORY_ADDRESS     FETCH(CAST(REGISTER_ADDRESS, REGISTER_TYPE))
#define MEMORY_RPIDATA     FETCH(CAST(REGISTER_RPIDATA, REGISTER_TYPE))
#define MEMORY_COMMAND     FETCH(CAST(REGISTER_COMMAND, REGISTER_TYPE))
#define MEMORY_ACCESS      FETCH(CAST(MEMORY_ADDRESS, MEMORY_TYPE))
#define MEMORY_TYPE        u32*

#define MAILBOX_WRITE      0
#define MAILBOX_READ       1
#define MAILBOX_IDLE       2

ENTRY
{
    MEMORY_COMMAND = MAILBOX_IDLE;
    WHILE (TRUE)
    {
        IF (MEMORY_COMMAND != MAILBOX_IDLE)
        {
            IF (MEMORY_COMMAND == MAILBOX_READ) // Python Read Command
            {
                 MEMORY_RPIDATA = MEMORY_ACCESS;
            }
            ELSE IF (MEMORY_COMMAND == MAILBOX_WRITE) // Python Write Command
            {
                 MEMORY_ACCESS = MEMORY_RPIDATA;
            }
            MEMORY_COMMAND = MAILBOX_IDLE;
        }
    }
    RETURN(0);
}
