import datetime
import duckdb
conn = duckdb.connect('file.db')
c = conn.cursor()

# CREATE
def create_sequence():
    c.execute('CREATE SEQUENCE id_sequence_sniplogs START 1')
    
def create_table():
	c.execute("create table if not exists sniplogs(rowid INTEGER DEFAULT nextval('id_sequence_sniplogs'), name TEXT, content TEXT, label TEXT, updt_dt DATE)")

def add(name, content, label, updt_dt):
	c.execute('insert into sniplogs(name, content, label, updt_dt) VALUES (?,?,?,?)',(name, content, label, updt_dt))
	conn.commit()

def insert(name, content, label):
    updt_dt = datetime.datetime.now().strftime('%Y-%m-%d')
    c.execute('insert into sniplogs (name, content, label, updt_dt) VALUES (?,?,?,?)',(name, content, label, updt_dt))
    conn.commit()

# READ
def view_all_data():
	c.execute('select * FROM sniplogs order by rowid desc')
	data = c.fetchall()
	return data

def view_all_names():
	c.execute('select distinct rowid, name FROM sniplogs order by rowid desc')
	data = c.fetchall()
	return data

def view_all_contents():
	c.execute('select distinct rowid, name FROM sniplogs order by rowid desc')
	data = c.fetchall()
	return data

def get_by_id(row_id):
	c.execute('select * FROM sniplogs WHERE rowid={}'.format(row_id))
	data = c.fetchall()
	return data

def get_content(content):
	c.execute("select * FROM sniplogs WHERE content='{}'".format(content))
	data = c.fetchall()
	return data

def get_label(label):
	c.execute("select * FROM sniplogs WHERE label='{}'".format(label))
	data = c.fetchall()

# UPDATE
def edit(new_name, new_content, new_label, new_updt_dt, new_rowid):
	c.execute('update sniplogs set name = ?, content =?, label=?, updt_dt=? WHERE rowid=?  ',(new_name, new_content, new_label, new_updt_dt, new_rowid))
	conn.commit()
	data = c.fetchall()
	return data

# DELETE    
def drop_table(): 
    c.execute('drop table sniplogs')
    conn.commit()
  
def delete_table():
    c.execute('delete from sniplogs where content is not null')
    conn.commit()

def delete_by_id(row_id):
	c.execute('delete from sniplogs WHERE rowid={}'.format(row_id))
	conn.commit()