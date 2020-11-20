# Point-of-Sale
Extremely basic, poorly written, Point of Sale system with a GUI that looks like it was made in 1998 or something. Manage items, users, transactions, etc.

## Instructions

<b>Dependencies:</b> Requires Python 3.x, sqlite3, datetime, tkinter, and tabulate.

### <b>How to use:</b> 
<ul>
  <li>Run createdb.py before doing anything else. This is required in order to create main.db, which contains the users, items, transactions, and sales tax tables.</li>
  <li>Run pos-start.py.</li>
  <li>Login with default credentials 1111, 1111.</li>
</ul>

### <b>How it works:</b>
<ul>
  <li><b>pos-start.py</b> launches <b>pos-login.py</b>, which authenticates user and launches <b>pos-mainmenu.py</b>.</li>
  <li><b>pos-mainmenu.py</b> launches <b>transaction.py</b>, <b>journalviewer.py</b>, <b>itemmaintenance.py</b>, <b>usermaintenance.py</b>, or <b>globalsettings.py</b>, based on user input.</li>
  <li><b>transaction.py</b> lists itemdb entries, prompts user for item selection, quantity, and payment method. Transactions are logged in transactiondb after confirmation. </li>
  <li><b>journalviewer.py</b> lists transactiondb entries. Filter by date or item. Refund will remove the transaction from the database.</li>
  <li><b>itemmaintenance.py</b> prompts user to either add, edit, remove, or view itemdb entries.</li>
  <li><b>usermaintenance.py</b> prompts user to either add, edit, remove, or view userdb entries.</li>
  <li><b>globalsettings.py</b> includes option for setting sales tax.</li>
</ul>

### <b>What I still have to do:</b>
<ul>
  <li>Database locks up pretty easily- especially when editing sales tax rate, for some reason.</li>
  <li>Consolidate variables; Lots of unnecessary variables in transaction.py from when I was first creating it on the CLI.</li>
  <li>Make the GUI less ugly.</li>
</ul>
