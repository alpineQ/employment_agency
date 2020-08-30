CREATE DATABASE EmploymentAgencyDB
GO
USE EmploymentAgencyDB

CREATE TABLE Agents
(
	AgentCode uniqueidentifier  NOT NULL ,
	SecondName nvarchar(20)  NOT NULL ,
	Name nvarchar(20)  NOT NULL ,
	Patronymic nvarchar(20)  NOT NULL ,
	PhoneNumber char(16)  NULL ,
	Email varchar(40)  NULL ,
	Sex nchar(1)  NULL
)
GO


ALTER TABLE Agents
	ADD CONSTRAINT Agents_AgentCode DEFAULT (NEWID()) FOR AgentCode
GO

ALTER TABLE Agents
	ADD CONSTRAINT AgentsKey PRIMARY KEY  CLUSTERED (AgentCode ASC)
GO


CREATE TABLE Applicants
(
	ApplicantCode uniqueidentifier  NOT NULL ,
	SecondName nvarchar(20) NOT NULL ,
	Name nvarchar(20) NOT NULL ,
	Patronymic nvarchar(20) NOT NULL ,
	ApplicationDate datetime  NULL ,
	Qualification nvarchar(20)  NULL ,
	Birthday datetime  NULL ,
	Sex nchar(1)  NOT NULL ,
	RegistrationAddress nvarchar(120)  NULL ,
	PhoneNumber char(16)  NULL ,
	JobExperience nvarchar(120)  NULL ,
	Email varchar(40)  NULL ,
	EducationCode uniqueidentifier  NULL ,
	PositionCode uniqueidentifier  NULL
)
GO


ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationDate DEFAULT (getdate()) FOR ApplicationDate
GO

ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationCode DEFAULT (NEWID()) FOR ApplicantCode
GO

ALTER TABLE Applicants
	ADD CONSTRAINT ApplicantsKey PRIMARY KEY  CLUSTERED (ApplicantCode ASC)
GO


CREATE TABLE Deals
(
	DealCode uniqueidentifier  NOT NULL ,
	IssueDate datetime  NULL ,
	CommissionFee integer  NULL ,
	WasPaid bit  NULL ,
	PaymentDate datetime  NULL ,
	ApplicantCode uniqueidentifier  NULL ,
	VacancyCode uniqueidentifier  NULL ,
	AgentCode uniqueidentifier  NULL
)
GO


ALTER TABLE Deals
	ADD CONSTRAINT Deals_DealCode DEFAULT (NEWID()) FOR DealCode
GO

ALTER TABLE Deals
	ADD CONSTRAINT DealsKey PRIMARY KEY  CLUSTERED (DealCode ASC)
GO


CREATE TABLE Education
(
	EducationCode uniqueidentifier  NOT NULL ,
	Education nvarchar(60)  NOT NULL ,
	Note nvarchar(120)  NULL ,
	EducationalInstitution char(18)  NULL 
)
GO


ALTER TABLE Education
	ADD CONSTRAINT Education_EducationCode DEFAULT (NEWID()) FOR EducationCode
GO

ALTER TABLE Education
	ADD CONSTRAINT EducationKey PRIMARY KEY  CLUSTERED (EducationCode ASC)
GO


CREATE TABLE Employers
(
	EmployerCode uniqueidentifier  NOT NULL ,
	EmployerOrganization nvarchar(60)  NOT NULL ,
	OrganizationAddress nvarchar(120)  NULL ,
	PhoneNumber char(16)  NULL ,
	Email varchar(40)  NULL ,
	License nvarchar(20)  NULL
)
GO


ALTER TABLE Employers
	ADD CONSTRAINT Employer_EmployerCode DEFAULT (NEWID()) FOR EmployerCode
GO

ALTER TABLE Employers
	ADD CONSTRAINT EmployersKey PRIMARY KEY  CLUSTERED (EmployerCode ASC)
GO


CREATE TABLE Positions
(
	PositionCode uniqueidentifier  NOT NULL ,
	PositionName nvarchar(60)  NULL ,
	Industry nvarchar(20)  NULL
)
GO


ALTER TABLE Positions
	ADD CONSTRAINT Positions_PositionCode DEFAULT (NEWID()) FOR PositionCode
GO

ALTER TABLE Positions
	ADD CONSTRAINT PositionsKey PRIMARY KEY  CLUSTERED (PositionCode ASC)
GO


CREATE TABLE Vacancies
(
	VacancyCode uniqueidentifier  NOT NULL ,
	PlacementDate datetime  NULL ,
	Salary money  NULL ,
	Schedule nvarchar(60)  NULL ,
	VacancyStatus nvarchar(60)  NOT NULL ,
	Industry nvarchar(20)  NULL ,
	RequiredEducation nvarchar(60)  NULL ,
	Qualification nvarchar(20)  NULL ,
	EmployerCode uniqueidentifier NULL
)
GO


ALTER TABLE Vacancies
	ADD CONSTRAINT Vacancies_VacancyCode DEFAULT (NEWID()) FOR VacancyCode
GO

ALTER TABLE Vacancies
	ADD CONSTRAINT VacanciesKey PRIMARY KEY  CLUSTERED (VacancyCode ASC)
GO