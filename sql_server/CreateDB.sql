CREATE DATABASE EmploymentAgencyDB
GO
USE EmploymentAgencyDB

CREATE TABLE Agents
(
	AgentCode char(18)  NOT NULL ,
	SecondName varchar(20)  NULL ,
	Name varchar(20)  NULL ,
	Patronymic varchar(20)  NULL ,
	PhoneNumber integer  NULL ,
	Email char(18)  NULL ,
	Sex char(18)  NULL 
)
go


ALTER TABLE Agents
	ADD CONSTRAINT Agents_AgentCode DEFAULT (NEWID()) FOR AgentCode
go

ALTER TABLE Agents
	ADD CONSTRAINT AgentsKey PRIMARY KEY  CLUSTERED (AgentCode ASC)
go


CREATE TABLE Applicants
(
	ApplicantCode uniqueidentifier  NOT NULL ,
	SecondName nvarchar(120)  NULL ,
	ApplicationDate datetime  NULL ,
	Name varchar(20)  NULL ,
	Patronymic varchar(20)  NULL ,
	Qualification varchar(20)  NULL ,
	Birthday datetime  NULL ,
	Sex varchar(20)  NULL ,
	RegistrationAddress nvarchar(120)  NULL ,
	PhoneNumber int  NULL ,
	JobExperience nvarchar(120)  NULL ,
	Email varchar(20)  NULL ,
	EducationCode uniqueidentifier  NOT NULL ,
	PositionCode char(18)  NOT NULL 
)
go


ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationDate DEFAULT (getdate()) FOR ApplicationDate
go

ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationCode DEFAULT (NEWID()) FOR ApplicantCode
go

ALTER TABLE Applicants
	ADD CONSTRAINT ApplicantsKey PRIMARY KEY  CLUSTERED (ApplicantCode ASC)
go


CREATE TABLE Deals
(
	DealCode char(18)  NOT NULL ,
	ApplicantCode uniqueidentifier  NOT NULL ,
	VacancyCode uniqueidentifier  NOT NULL ,
	IssueDate datetime  NULL ,
	CommissionFee integer  NULL ,
	WasPaid char(18)  NULL ,
	PaymentDate datetime  NULL ,
	AgentCode char(18)  NOT NULL 
)
go


ALTER TABLE Deals
	ADD CONSTRAINT Deals_DealCode DEFAULT (NEWID()) FOR DealCode
go

ALTER TABLE Deals
	ADD CONSTRAINT DealsKey PRIMARY KEY  CLUSTERED (DealCode ASC)
go


CREATE TABLE Education
(
	EducationCode uniqueidentifier  NOT NULL ,
	Education nvarchar(60)  NOT NULL ,
	Note nvarchar(120)  NULL ,
	EducationalInstitution char(18)  NULL 
)
go


ALTER TABLE Education
	ADD CONSTRAINT Education_EducationCode DEFAULT (NEWID()) FOR EducationCode
go

ALTER TABLE Education
	ADD CONSTRAINT EducationKey PRIMARY KEY  CLUSTERED (EducationCode ASC)
go


CREATE TABLE Employers
(
	EmployerCode uniqueidentifier  NOT NULL ,
	EmployerOrganization nvarchar(60)  NOT NULL ,
	OrganizationAddress nvarchar(120)  NULL ,
	PhoneNumber int  NULL ,
	Email varchar(60)  NULL ,
	License varchar(20)  NULL 
)
go


ALTER TABLE Employers
	ADD CONSTRAINT Employer_EmployerCode DEFAULT (NEWID()) FOR EmployerCode
go

ALTER TABLE Employers
	ADD CONSTRAINT EmployersKey PRIMARY KEY  CLUSTERED (EmployerCode ASC)
go


CREATE TABLE Positions
(
	PositionCode char(18)  NOT NULL ,
	PositionName varchar(20)  NULL ,
	Industry varchar(20)  NULL 
)
go


ALTER TABLE Positions
	ADD CONSTRAINT Positions_PositionCode DEFAULT (NEWID()) FOR PositionCode
go

ALTER TABLE Positions
	ADD CONSTRAINT PositionsKey PRIMARY KEY  CLUSTERED (PositionCode ASC)
go


CREATE TABLE Vacancies
(
	VacancyCode uniqueidentifier  NOT NULL ,
	PlacementDate datetime  NULL ,
	Salary money  NULL ,
	Schedule nvarchar(60)  NULL ,
	VacancyStatus nvarchar(60)  NOT NULL ,
	Industry varchar(20)  NULL ,
	RequiredEducation varchar(20)  NULL ,
	Qualification varchar(20)  NULL ,
	EmployerCode uniqueidentifier  NOT NULL 
)
go


ALTER TABLE Vacancies
	ADD CONSTRAINT Vacancies_VacancyCode DEFAULT (NEWID()) FOR VacancyCode
go

ALTER TABLE Vacancies
	ADD CONSTRAINT VacanciesKey PRIMARY KEY  CLUSTERED (VacancyCode ASC)
go



ALTER TABLE Applicants
	ADD CONSTRAINT  R_12 FOREIGN KEY (EducationCode) REFERENCES Education(EducationCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE Applicants
	ADD CONSTRAINT  R_17 FOREIGN KEY (PositionCode) REFERENCES Positions(PositionCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go



ALTER TABLE Deals
	ADD CONSTRAINT  R_8 FOREIGN KEY (VacancyCode) REFERENCES Vacancies(VacancyCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE Deals
	ADD CONSTRAINT  R_14 FOREIGN KEY (AgentCode) REFERENCES Agents(AgentCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE Deals
	ADD CONSTRAINT  R_18 FOREIGN KEY (ApplicantCode) REFERENCES Applicants(ApplicantCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go



ALTER TABLE Vacancies
	ADD CONSTRAINT  R_13 FOREIGN KEY (EmployerCode) REFERENCES Employers(EmployerCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go
