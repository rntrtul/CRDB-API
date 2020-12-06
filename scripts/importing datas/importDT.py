import xlrd


C1DIR = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/C1/Damage Taken -Tal'Dorei.xls"
C2DIR = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/C2/Damage Taken - Wildemount.xls"
C1HeaderRow = 0
C2HeaderRow = 2

curr_dir = C1DIR
curr_head_row = C1HeaderRow
curr_camp = 1

book = xlrd.open_workbook(curr_dir, formatting_info=True)
sheets = book.sheet_names()

def get_damage_type_colors(row_start, sheet, col, camp):
  colors = {}
  for row in range(rows):
    cell = sheet.cell(row_start+ row, col)
    colors[get_cell_color(cell)] = cell.value

def get_cell_color(cell):
  xfx = cell.xf_index
  xf = book.xf_list[xfx]
  bgx = xf.background.pattern_colour_index
  return bgx

def get_font_color(cell):
  xf = book.xf_list[cell.xf_index]
  font = book.font_list[xf.font_index]
  return book.colour_map.get(font.colour_index)
  
def get_cell_comment(row,col, sheet):
  notes = sheet.cell_note_map
  if (row,col) in notes:
    return notes[(row,col)].text
  else:
    return ""

def get_headers (sheet):
  headers = {}
  dmg_type_color_map = {}

  row_start = 0
  dmg_col_header = "Key"
  dmg_col_rows = 12

  if curr_camp == 2:
    row_start = 1
    dmg_col_header = "Damage type"
    dmg_col_rows = 11

  for col in range(sheet.ncols):
    cell = sheet.cell(row_start, col)
    headers[col] = cell.value
    headers[cell.value] = col

  dmg_header = headers[dmg_col_header]
  for row in range(dmg_col_rows):
    cell = sheet.cell(row, dmg_header)
    print(cell)
    #get everything befoer = sign
    dmg_type_color_map[get_cell_color(cell)] = cell.value

  print("Damage:", dmg_type_color_map)

  return headers, dmg_type_color_map

print ("Sheets are:", sheets)

for index, sh in enumerate(sheets):
  if sh in ['Total', 'Total S1', 'Total S2', 'Total S3']:
    continue

  sheet = book.sheet_by_index(index)
  rows, cols = sheet.nrows, sheet.ncols
  print("Sheet", sheet.name)
  
  row_start = 1
  if curr_camp == 2:
    row_start = 2
  
  headers, dmg_colors = get_headers(sheet)

  for row in range(row_start, rows):
    for col in range(cols):
      cell = sheet.cell(row, col)
      color = get_cell_color(cell)
      comment = get_cell_comment(row,col,sheet)
      font_color = get_font_color(cell)

      #print("row, col is:", row+1, col+1, "color is:", color, "value is:", cell.value, "comment is:", comment, "font color:", font_color)
