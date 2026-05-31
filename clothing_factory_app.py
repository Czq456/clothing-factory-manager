import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

class ClothingFactoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("服装厂生产管理系统")
        self.root.geometry("1100x650")
        self.root.minsize(900, 500)

        self.conn = sqlite3.connect('clothing_factory.db')
        self.cursor = self.conn.cursor()
        self.init_database()
        self.create_widgets()
        self.load_data()

    def init_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS styles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                unit_price REAL NOT NULL,
                cost REAL NOT NULL,
                description TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS production (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_name TEXT NOT NULL,
                style_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                record_date TEXT NOT NULL,
                FOREIGN KEY (style_id) REFERENCES styles(id)
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_production = ttk.Frame(self.notebook)
        self.tab_styles = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_production, text='📝 生产记录')
        self.notebook.add(self.tab_styles, text='👕 款型管理')

        self.create_production_tab()
        self.create_styles_tab()
        self.load_data()

    def create_production_tab(self):
        main_frame = ttk.Frame(self.tab_production)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(btn_frame, text='添加记录', command=self.add_record).pack(side='left', padx=3)
        ttk.Button(btn_frame, text='删除记录', command=self.delete_record).pack(side='left', padx=3)
        ttk.Button(btn_frame, text='刷新', command=self.load_data).pack(side='left', padx=3)

        filter_frame = ttk.Frame(btn_frame)
        filter_frame.pack(side='right', padx=3)
        ttk.Label(filter_frame, text='日期:').pack(side='left', padx=2)
        self.date_filter = ttk.Entry(filter_frame, width=12)
        self.date_filter.pack(side='left', padx=2)
        self.date_filter.insert(0, datetime.now().strftime('%Y-%m-%d'))
        ttk.Button(filter_frame, text='筛选', command=self.load_data).pack(side='left', padx=2)
        ttk.Button(filter_frame, text='全部', command=self.show_all).pack(side='left', padx=2)

        stats_frame = ttk.LabelFrame(main_frame, text='统计')
        stats_frame.pack(fill='x', pady=(0, 10))

        self.stat_labels = {}
        stats_info = [
            ('count', '记录数'),
            ('quantity', '总数量'),
            ('amount', '总金额'),
            ('cost', '总成本'),
            ('profit', '总利润')
        ]
        for key, label in stats_info:
            f = ttk.Frame(stats_frame)
            f.pack(side='left', padx=15, pady=5)
            ttk.Label(f, text=f'{label}:', font=('Microsoft YaHei', 9, 'bold')).pack(side='left')
            self.stat_labels[key] = ttk.Label(f, text='0', font=('Microsoft YaHei', 9), width=10)
            self.stat_labels[key].pack(side='left', padx=5)

        columns = ('id', 'worker', 'date', 'style', 'quantity', 'price', 'amount', 'cost', 'profit')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)

        self.tree.heading('id', text='序号')
        self.tree.heading('worker', text='工人姓名')
        self.tree.heading('date', text='日期')
        self.tree.heading('style', text='款型')
        self.tree.heading('quantity', text='数量')
        self.tree.heading('price', text='单价')
        self.tree.heading('amount', text='金额')
        self.tree.heading('cost', text='成本')
        self.tree.heading('profit', text='利润')

        self.tree.column('id', width=50, anchor='center')
        self.tree.column('worker', width=100)
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('style', width=120)
        self.tree.column('quantity', width=60, anchor='center')
        self.tree.column('price', width=80, anchor='e')
        self.tree.column('amount', width=90, anchor='e')
        self.tree.column('cost', width=80, anchor='e')
        self.tree.column('profit', width=80, anchor='e')

        style = ttk.Style()
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Microsoft YaHei', 9, 'bold'))

        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        bottom_frame = ttk.LabelFrame(main_frame, text='工资结算')
        bottom_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(bottom_frame, text='按工人查工资', command=self.query_by_worker).pack(side='left', padx=5, pady=5)
        ttk.Button(bottom_frame, text='按月份查工资', command=self.query_by_month).pack(side='left', padx=5, pady=5)
        ttk.Button(bottom_frame, text='导出工资表', command=self.export_wages).pack(side='left', padx=5, pady=5)

        self.wages_text = tk.Text(bottom_frame, height=4, font=('Microsoft YaHei', 9))
        self.wages_text.pack(fill='x', padx=5, pady=5)

    def create_styles_tab(self):
        main_frame = ttk.Frame(self.tab_styles)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(btn_frame, text='添加款型', command=self.add_style).pack(side='left', padx=3)
        ttk.Button(btn_frame, text='编辑款型', command=self.edit_style).pack(side='left', padx=3)
        ttk.Button(btn_frame, text='删除款型', command=self.delete_style).pack(side='left', padx=3)

        columns = ('id', 'name', 'price', 'cost', 'desc')
        self.styles_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)

        self.styles_tree.heading('id', text='序号')
        self.styles_tree.heading('name', text='款型名称')
        self.styles_tree.heading('price', text='单价')
        self.styles_tree.heading('cost', text='成本')
        self.styles_tree.heading('desc', text='描述')

        self.styles_tree.column('id', width=50, anchor='center')
        self.styles_tree.column('name', width=150)
        self.styles_tree.column('price', width=100, anchor='e')
        self.styles_tree.column('cost', width=100, anchor='e')
        self.styles_tree.column('desc', width=200)

        style = ttk.Style()
        style.configure('Treeview', rowheight=28)
        style.configure('Treeview.Heading', font=('Microsoft YaHei', 9, 'bold'))

        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.styles_tree.yview)
        self.styles_tree.configure(yscrollcommand=scrollbar.set)
        self.styles_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.load_styles_data()

    def load_styles_data(self):
        for item in self.styles_tree.get_children():
            self.styles_tree.delete(item)
        self.cursor.execute('SELECT id, name, unit_price, cost, COALESCE(description, \'\') FROM styles ORDER BY id')
        for row in self.cursor.fetchall():
            self.styles_tree.insert('', 'end', values=row)

    def add_style(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('添加款型')
        dialog.geometry('400x250')
        dialog.transient(self.root)
        dialog.grab_set()

        f = ttk.Frame(dialog, padding=20)
        f.pack(fill='both', expand=True)

        ttk.Label(f, text='款型名称:').grid(row=0, column=0, sticky='e', pady=8)
        name_entry = ttk.Entry(f, width=25)
        name_entry.grid(row=0, column=1, pady=8)
        name_entry.focus()

        ttk.Label(f, text='单价:').grid(row=1, column=0, sticky='e', pady=8)
        price_entry = ttk.Entry(f, width=25)
        price_entry.grid(row=1, column=1, pady=8)

        ttk.Label(f, text='成本:').grid(row=2, column=0, sticky='e', pady=8)
        cost_entry = ttk.Entry(f, width=25)
        cost_entry.grid(row=2, column=1, pady=8)

        ttk.Label(f, text='描述:').grid(row=3, column=0, sticky='e', pady=8)
        desc_entry = ttk.Entry(f, width=25)
        desc_entry.grid(row=3, column=1, pady=8)

        def save():
            name = name_entry.get().strip()
            try:
                price = float(price_entry.get().strip())
                cost = float(cost_entry.get().strip())
            except ValueError:
                messagebox.showerror('错误', '单价和成本必须是数字')
                return
            desc = desc_entry.get().strip()

            if not name:
                messagebox.showerror('错误', '款型名称不能为空')
                return
            if price <= 0 or cost <= 0:
                messagebox.showerror('错误', '单价和成本必须大于0')
                return

            try:
                self.cursor.execute(
                    'INSERT INTO styles (name, unit_price, cost, description) VALUES (?, ?, ?, ?)',
                    (name, price, cost, desc)
                )
                self.conn.commit()
                self.load_styles_data()
                dialog.destroy()
                messagebox.showinfo('成功', '款型已添加')
            except sqlite3.IntegrityError:
                messagebox.showerror('错误', '款型名称已存在')

        ttk.Button(f, text='保存', command=save).grid(row=4, column=0, columnspan=2, pady=15)

    def edit_style(self):
        selection = self.styles_tree.selection()
        if not selection:
            messagebox.showwarning('提示', '请先选择一条款型')
            return

        item = self.styles_tree.item(selection[0])
        values = item['values']
        style_id, old_name, old_price, old_cost, old_desc = values

        dialog = tk.Toplevel(self.root)
        dialog.title('编辑款型')
        dialog.geometry('400x250')
        dialog.transient(self.root)
        dialog.grab_set()

        f = ttk.Frame(dialog, padding=20)
        f.pack(fill='both', expand=True)

        ttk.Label(f, text='款型名称:').grid(row=0, column=0, sticky='e', pady=8)
        name_entry = ttk.Entry(f, width=25)
        name_entry.grid(row=0, column=1, pady=8)
        name_entry.insert(0, old_name)

        ttk.Label(f, text='单价:').grid(row=1, column=0, sticky='e', pady=8)
        price_entry = ttk.Entry(f, width=25)
        price_entry.grid(row=1, column=1, pady=8)
        price_entry.insert(0, str(old_price))

        ttk.Label(f, text='成本:').grid(row=2, column=0, sticky='e', pady=8)
        cost_entry = ttk.Entry(f, width=25)
        cost_entry.grid(row=2, column=1, pady=8)
        cost_entry.insert(0, str(old_cost))

        ttk.Label(f, text='描述:').grid(row=3, column=0, sticky='e', pady=8)
        desc_entry = ttk.Entry(f, width=25)
        desc_entry.grid(row=3, column=1, pady=8)
        desc_entry.insert(0, old_desc)

        def save():
            name = name_entry.get().strip()
            try:
                price = float(price_entry.get().strip())
                cost = float(cost_entry.get().strip())
            except ValueError:
                messagebox.showerror('错误', '单价和成本必须是数字')
                return
            desc = desc_entry.get().strip()

            if not name:
                messagebox.showerror('错误', '款型名称不能为空')
                return
            if price <= 0 or cost <= 0:
                messagebox.showerror('错误', '单价和成本必须大于0')
                return

            try:
                self.cursor.execute(
                    'UPDATE styles SET name=?, unit_price=?, cost=?, description=? WHERE id=?',
                    (name, price, cost, desc, style_id)
                )
                self.conn.commit()
                self.load_styles_data()
                dialog.destroy()
                messagebox.showinfo('成功', '款型已更新')
            except sqlite3.IntegrityError:
                messagebox.showerror('错误', '款型名称已存在')

        ttk.Button(f, text='保存', command=save).grid(row=4, column=0, columnspan=2, pady=15)

    def delete_style(self):
        selection = self.styles_tree.selection()
        if not selection:
            messagebox.showwarning('提示', '请先选择一条款型')
            return

        item = self.styles_tree.item(selection[0])
        style_id = item['values'][0]

        if messagebox.askyesno('确认', '确定要删除这个款型吗？'):
            self.cursor.execute('DELETE FROM styles WHERE id = ?', (style_id,))
            self.conn.commit()
            self.load_styles_data()
            messagebox.showinfo('成功', '款型已删除')

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        date_filter = self.date_filter.get().strip()

        if date_filter:
            sql = '''
                SELECT p.id, p.worker_name, p.record_date, s.name, p.quantity, s.unit_price,
                       p.quantity * s.unit_price, p.quantity * s.cost, p.quantity * (s.unit_price - s.cost)
                FROM production p JOIN styles s ON p.style_id = s.id
                WHERE p.record_date = ?
                ORDER BY p.worker_name, p.id
            '''
            self.cursor.execute(sql, (date_filter,))
        else:
            sql = '''
                SELECT p.id, p.worker_name, p.record_date, s.name, p.quantity, s.unit_price,
                       p.quantity * s.unit_price, p.quantity * s.cost, p.quantity * (s.unit_price - s.cost)
                FROM production p JOIN styles s ON p.style_id = s.id
                ORDER BY p.worker_name, p.id
            '''
            self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

        total_count = len(rows)
        total_qty = sum(r[4] for r in rows)
        total_amount = sum(r[6] for r in rows)
        total_cost = sum(r[7] for r in rows)
        total_profit = sum(r[8] for r in rows)

        self.stat_labels['count'].config(text=str(total_count))
        self.stat_labels['quantity'].config(text=f'{total_qty}件')
        self.stat_labels['amount'].config(text=f'{total_amount:.2f}元')
        self.stat_labels['cost'].config(text=f'{total_cost:.2f}元')
        self.stat_labels['profit'].config(text=f'{total_profit:.2f}元')

        self.wages_text.delete('1.0', 'end')

    def show_all(self):
        self.date_filter.delete(0, 'end')
        self.load_data()

    def add_record(self):
        self.cursor.execute('SELECT id, name, unit_price FROM styles ORDER BY id')
        styles = self.cursor.fetchall()
        if not styles:
            messagebox.showwarning('提示', '请先在款型管理中添加款型')
            return

        dialog = tk.Toplevel(self.root)
        dialog.title('添加记录')
        dialog.geometry('400x300')
        dialog.transient(self.root)
        dialog.grab_set()

        f = ttk.Frame(dialog, padding=20)
        f.pack(fill='both', expand=True)

        ttk.Label(f, text='工人姓名:').grid(row=0, column=0, sticky='e', pady=8)
        worker_entry = ttk.Entry(f, width=20)
        worker_entry.grid(row=0, column=1, pady=8)
        worker_entry.focus()

        ttk.Label(f, text='款型:').grid(row=1, column=0, sticky='e', pady=8)
        style_var = tk.StringVar()
        style_combo = ttk.Combobox(f, textvariable=style_var, values=[s[1] for s in styles],
                                    width=18, state='readonly')
        style_combo.grid(row=1, column=1, pady=8)
        style_combo.current(0)

        ttk.Label(f, text='数量:').grid(row=2, column=0, sticky='e', pady=8)
        qty_entry = ttk.Entry(f, width=20)
        qty_entry.grid(row=2, column=1, pady=8)

        ttk.Label(f, text='日期:').grid(row=3, column=0, sticky='e', pady=8)
        date_entry = ttk.Entry(f, width=20)
        date_entry.grid(row=3, column=1, pady=8)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        def save():
            worker = worker_entry.get().strip()
            style_name = style_var.get()
            try:
                qty = int(qty_entry.get().strip())
            except ValueError:
                messagebox.showerror('错误', '数量必须是整数')
                return
            date = date_entry.get().strip()

            if not worker:
                messagebox.showerror('错误', '工人姓名不能为空')
                return
            if qty <= 0:
                messagebox.showerror('错误', '数量必须大于0')
                return
            if not date:
                messagebox.showerror('错误', '日期不能为空')
                return

            style_id = next(s[0] for s in styles if s[1] == style_name)
            self.cursor.execute(
                'INSERT INTO production (worker_name, style_id, quantity, record_date) VALUES (?, ?, ?, ?)',
                (worker, style_id, qty, date)
            )
            self.conn.commit()
            dialog.destroy()
            self.load_data()
            messagebox.showinfo('成功', '记录已添加')

        ttk.Button(f, text='保存', command=save).grid(row=4, column=0, columnspan=2, pady=15)

    def delete_record(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning('提示', '请先选择一条记录')
            return

        item = self.tree.item(selection[0])
        record_id = item['values'][0]

        if messagebox.askyesno('确认', '确定要删除这条记录吗？'):
            self.cursor.execute('DELETE FROM production WHERE id = ?', (record_id,))
            self.conn.commit()
            self.load_data()
            messagebox.showinfo('成功', '记录已删除')

    def query_by_worker(self):
        name = simpledialog.askstring('查询', '请输入工人姓名:', parent=self.root)
        if not name:
            return

        self.cursor.execute('''
            SELECT p.record_date, s.name, p.quantity, s.unit_price, p.quantity * s.unit_price
            FROM production p JOIN styles s ON p.style_id = s.id
            WHERE p.worker_name = ?
            ORDER BY p.record_date DESC
        ''', (name,))

        records = self.cursor.fetchall()
        self.wages_text.delete('1.0', 'end')

        if not records:
            self.wages_text.insert('end', f'未找到工人 "{name}" 的记录\n')
            return

        total = sum(r[4] for r in records)
        self.wages_text.insert('end', f'=== {name} 工资明细 ===\n\n')
        self.wages_text.insert('end', f"{'日期':<12} {'款型':<12} {'数量':<6} {'单价':<8} {'金额':<10}\n")
        self.wages_text.insert('end', '-' * 50 + '\n')
        for r in records:
            self.wages_text.insert('end', f'{r[0]:<12} {r[1]:<12} {r[2]:<6} {r[3]:<8.2f} {r[4]:<10.2f}\n')
        self.wages_text.insert('end', '-' * 50 + '\n')
        self.wages_text.insert('end', f'合计工资: {total:.2f} 元\n')

    def query_by_month(self):
        month = simpledialog.askstring('查询', '请输入月份(如 2024-01):', parent=self.root)
        if not month:
            return

        self.cursor.execute('''
            SELECT worker_name, SUM(p.quantity * s.unit_price) as total
            FROM production p JOIN styles s ON p.style_id = s.id
            WHERE p.record_date LIKE ?
            GROUP BY worker_name
            ORDER BY total DESC
        ''', (f'{month}%',))

        records = self.cursor.fetchall()
        self.wages_text.delete('1.0', 'end')

        if not records:
            self.wages_text.insert('end', f'{month} 月没有生产记录\n')
            return

        grand_total = sum(r[1] for r in records)
        self.wages_text.insert('end', f'=== {month} 月工资表 ===\n\n')
        self.wages_text.insert('end', f"{'工人姓名':<15} {'工资(元)':<15}\n")
        self.wages_text.insert('end', '-' * 35 + '\n')
        for r in records:
            self.wages_text.insert('end', f'{r[0]:<15} {r[1]:<15.2f}\n')
        self.wages_text.insert('end', '-' * 35 + '\n')
        self.wages_text.insert('end', f'工资总计: {grand_total:.2f} 元\n')

    def export_wages(self):
        month = simpledialog.askstring('导出', '请输入月份(如 2024-01):', parent=self.root)
        if not month:
            return

        self.cursor.execute('''
            SELECT worker_name, SUM(p.quantity * s.unit_price) as total
            FROM production p JOIN styles s ON p.style_id = s.id
            WHERE p.record_date LIKE ?
            GROUP BY worker_name
            ORDER BY total DESC
        ''', (f'{month}%',))

        records = self.cursor.fetchall()
        if not records:
            messagebox.showinfo('提示', f'{month} 月没有生产记录')
            return

        filename = f'工资表_{month}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'=== {month} 月工资表 ===\n\n')
            f.write(f"{'工人姓名':<15} {'工资(元)':<15}\n")
            f.write('-' * 35 + '\n')
            grand_total = 0
            for r in records:
                f.write(f'{r[0]:<15} {r[1]:<15.2f}\n')
                grand_total += r[1]
            f.write('-' * 35 + '\n')
            f.write(f'工资总计: {grand_total:.2f} 元\n')

        messagebox.showinfo('成功', f'已导出到 {filename}')

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = ClothingFactoryApp(root)
    root.mainloop()
