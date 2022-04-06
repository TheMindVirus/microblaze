#define TRUE                    1
#define FALSE                   0

#define ENTRY                   void main()
#define POINTER(X)              *(volatile unsigned*)(X)

#define IF                      if
#define ELSE                    else
#define WHILE                   while

#define MEMORY_ADDRESS          0x0000FFF8
#define MEMORY_RPIDATA          0x0000FF00
#define MEMORY_COMMAND          0x0000FFFC

#define MAILBOX_ADDRESS         POINTER(MEMORY_ADDRESS)
#define MAILBOX_RPIDATA         POINTER(MEMORY_RPIDATA)
#define MAILBOX_COMMAND         POINTER(MEMORY_COMMAND)

#define MAILBOX_COMMAND_READ    0
#define MAILBOX_COMMAND_WRITE   1
#define MAILBOX_COMMAND_IDLE    2

ENTRY
{
    MAILBOX_COMMAND = MAILBOX_COMMAND_IDLE;
    WHILE (TRUE)
    {
        IF (MAILBOX_COMMAND != MAILBOX_COMMAND_IDLE)
        {
            IF (MAILBOX_COMMAND == MAILBOX_COMMAND_READ) // Python Read Command
            {
                 MAILBOX_RPIDATA = POINTER(MAILBOX_ADDRESS);
            }
            ELSE IF (MAILBOX_COMMAND == MAILBOX_COMMAND_WRITE) // Python Write Command
            {
                 POINTER(MAILBOX_ADDRESS) = MAILBOX_RPIDATA;
            }
        }
        MAILBOX_COMMAND = MAILBOX_COMMAND_IDLE;
    }
}
