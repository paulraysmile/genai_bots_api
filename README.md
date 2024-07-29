# genai_bots_api
1、初始prompt为提供的对话文件生成
2、安装mysql5.7
3、运行如下mysql语句
CREATE DATABASE genai DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'genai'@'%' IDENTIFIED BY 'scyz_ai';
GRANT ALL PRIVILEGES ON genai.* TO 'genai'@'%';

CREATE TABLE system_instruction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(50) NOT NULL,
    instruction TEXT NOT NULL
);


CREATE TABLE btc_convo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(255),
    role ENUM('model', 'user'),
    parts TEXT
);

CREATE TABLE eth_convo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(255),
    role ENUM('model', 'user'),
    parts TEXT
);

CREATE TABLE pepe_convo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(255),
    role ENUM('model', 'user'),
    parts TEXT
);

CREATE TABLE doge_convo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(255),
    role ENUM('model', 'user'),
    parts TEXT
);

CREATE TABLE sol_convo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_name VARCHAR(255),
    role ENUM('model', 'user'),
    parts TEXT
);

4、表说明：
 a、system_instruction 定义AI角色性格等信息
 b、**_convo 对应的AI角色回话记录，用于后续调整prompt进行微调

5、启动
 a、 修改代码db_utils.py中数据路连接信息
 b、 export GENAI_API_KEY=AIzaSyCjEqX8RjkpnpZXPPPdksNnNhoXmMEASbs
 c、 uvicorn run:app --host 0.0.0.0 --port 8000 --reload

6、浏览器访问一下连接，获取接口说明信息
{IP}:8000/docs

7、待完善
 a、增加页面用于配置mysql，GENAI_API_KEY, 导出json格式回话记录并上传prompt
 b、增加功能可以自定义修改genai参数