import duckdb
conn = duckdb.connect('file.db')
c = conn.cursor()

# CREATE
def create_sequence():
    c.execute('CREATE SEQUENCE id_sequence_snippets START 1')
    
def create_table():
	c.execute("create table if not exists snippets(rowid INTEGER DEFAULT nextval('id_sequence_snippets'), name TEXT, content TEXT, label TEXT, updt_dt DATE)")

def add(name, content, label, updt_dt):
	c.execute('insert into snippets(name, content, label, updt_dt) VALUES (?,?,?,?)',(name, content, label, updt_dt))
	conn.commit()
    
# READ
def view_all_data():
	c.execute('select * FROM snippets order by rowid desc')
	data = c.fetchall()
	return data

def view_all_names():
	c.execute('select distinct rowid, name FROM snippets order by rowid desc')
	data = c.fetchall()
	return data

def get_by_id(row_id):
	c.execute('select * FROM snippets WHERE rowid={}'.format(row_id))
	data = c.fetchall()
	return data

def get_content(content):
	c.execute("select * FROM snippets WHERE content='{}'".format(content))
	data = c.fetchall()
	return data

def get_label(label):
	c.execute("select * FROM snippets WHERE label='{}'".format(label))
	data = c.fetchall()

# UPDATE
def edit(new_name, new_content, new_label, new_updt_dt, new_rowid):
	c.execute('update snippets set name = ?, content =?, label=?, updt_dt=? WHERE rowid=?  ',(new_name, new_content, new_label, new_updt_dt, new_rowid))
	conn.commit()
	data = c.fetchall()
	return data

# DELETE    
def drop_table(): 
    c.execute('drop table snippets')
    conn.commit()
  
def delete_table():
    c.execute('delete from snippets where content is not null')
    conn.commit()

def delete_by_id(row_id):
	c.execute('delete from snippets WHERE rowid={}'.format(row_id))
	conn.commit()