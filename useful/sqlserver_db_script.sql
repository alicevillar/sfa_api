CREATE DATABASE SFA_DB;
USE SFA_DB;

CREATE TABLE TB_SFA_Images  (
Ima_Id int identity(1,1),
Ima_Copyright varchar (100),
Ima_Date date,
Ima_Explanation varchar (2000) not null,
Ima_Title varchar (100) not null,
Ima_Url varchar (300) not null,
constraint TB_Images primary key clustered (Ima_Id)
);

CREATE TABLE TB_SFA_Registration  (
Reg_Id int identity(1,1),
Reg_Name varchar (100) not null,
Reg_LastName varchar (100) not null,
Reg_Email varchar (100) not null,
Reg_Authentication_Key varchar (100),
Reg_Expiration_Date date not null,
Reg_Last_Access_Ip varchar (15) not null, 
Reg_Is_Blocked bit not null, 
Reg_Password varchar (100) not null,
constraint SFA_Registration primary key clustered (Reg_Id)
);

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [Reg_Authentication_Key] FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = 'TUsVsZ-Br4QXjqdWdpkEC2uBb7V97v2Fa4qQIgsZ' COLLATE Latin1_General_CS_AS ;

SELECT Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = 'TUsVsZ-Br4QXjqdWdpkEC2uBb7V97v2Fa4qQIgsZ' COLLATE Latin1_General_CS_AS 
 
