
def InitTable(db):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS user")

    # 使用预处理语句创建表
    usersql = """CREATE TABLE user (
    ID int AUTO_INCREMENT PRIMARY KEY,
    username varchar(32) NOT NULL,
    password TEXT NOT NULL
)ENGINE=INNODB DEFAULT CHARSET=utf8;"""

    cursor.execute(usersql)
    cursor.execute("DROP TABLE IF EXISTS banner_table")
    bannersql = """CREATE TABLE `banner_table`  (
  `ID` int(11) AUTO_INCREMENT PRIMARY KEY ,
  `title` varchar(32)  NOT NULL ,
  `description` varchar(300)  NOT NULL ,
  `href` varchar(300)  NOT NULL 
) ENGINE = InnoDB  CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"""

    cursor.execute(bannersql)
    cursor.execute("DROP TABLE IF EXISTS `custom_table`;")
    CustomSql = """CREATE TABLE `custom_table`  (
      `ID` int(10) AUTO_INCREMENT PRIMARY KEY,
      `title` varchar(32) NOT NULL,
      `description` varchar(200) NOT NULL,
      `src` varchar(300) NOT NULL
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
    """
    cursor.execute(CustomSql)