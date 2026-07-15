# Point of Sale Troubleshooting

## Error E-102 Card Reader Timeout
Error E-102 indicates the card reader lost communication with the terminal. Unplug
the reader cable from the back of the terminal, wait ten seconds, and reconnect.
If the error persists, reboot the terminal from the manager menu. Do not power cycle
the terminal from the wall outlet, which can corrupt the offline transaction cache.

## Error E-215 Offline Mode
Error E-215 means the terminal has lost its network connection and has entered
offline mode. Transactions continue to process and queue locally. The queue holds a
maximum of 200 transactions. When the network returns, the terminal syncs
automatically. If the queue reaches capacity, stop taking card payments and switch
to the backup terminal.

## Error E-330 Drawer Will Not Open
Error E-330 is a cash drawer solenoid fault. Verify the drawer cable is seated in
port RJ-12 on the underside of the terminal. Use the manual release key only with
a supervisor present, and record the opening in the exception log.

## Receipt Printer Jams
For a paper jam, open the printer lid, remove the partial roll, and clear any torn
paper from the cutter. Reload with the glossy side facing the print head. A printer
that feeds blank paper is loaded upside down.

## Terminal Reboot Procedure
Reboot only from Manager Menu, option 9, Restart Terminal. A proper reboot flushes
the offline queue first. Hard power cycling risks losing queued transactions and
requires a reconciliation ticket.

## Escalation
If an error code is not listed here, capture the code, the terminal number, and the
time, and open a ticket with the help desk. Terminal hardware failures are replaced
within one business day under the service contract.
