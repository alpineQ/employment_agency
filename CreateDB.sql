CREATE DATABASE EmploymentAgencyDB
go
USE EmploymentAgencyDB

CREATE TABLE Applicants
(
	ApplicantCode uniqueidentifier  NOT NULL ,
	ApplicantFullName nvarchar(120)  NOT NULL ,
	ApplicationDate datetime  NULL ,
	PositionCode uniqueidentifier  NULL ,
	JobExperience nvarchar(120)  NULL 
)
go


ALTER TABLE Applicants
	ADD CONSTRAINT S1 PRIMARY KEY  CLUSTERED (ApplicantCode ASC)
go

ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationDate DEFAULT (getdate()) FOR ApplicationDate
go

ALTER TABLE Applicants
	ADD CONSTRAINT Applicants_ApplicationCode DEFAULT (NEWID()) FOR ApplicantCode
go

CREATE TABLE ApplicantData
(
	ApplicantCode uniqueidentifier  NOT NULL ,
	Birthday datetime  NULL ,
	RegistrationAddress nvarchar(120)  NULL ,
	PhoneNumber int  NULL ,
	EducationCode uniqueidentifier  NOT NULL
)
go

ALTER TABLE ApplicantData
	ADD CONSTRAINT ApplicantData_ApplicationCode DEFAULT (NEWID()) FOR ApplicantCode
go


ALTER TABLE ApplicantData
	ADD CONSTRAINT S2 PRIMARY KEY  CLUSTERED (ApplicantCode ASC)
go


CREATE TABLE EducationData
(
	EducationCode uniqueidentifier  NOT NULL ,
	Education nvarchar(60)  NOT NULL ,
	Note nvarchar(120)  NULL 
)
go

ALTER TABLE EducationData
	ADD CONSTRAINT EducationData_EducationCode DEFAULT (NEWID()) FOR EducationCode
go


ALTER TABLE EducationData
	ADD CONSTRAINT S3 PRIMARY KEY  CLUSTERED (EducationCode ASC)
go


CREATE TABLE Employers
(
	EmployerCode uniqueidentifier  NOT NULL ,
	EmployerOrganization nvarchar(60)  NOT NULL ,
	OrganizationAddress nvarchar(120)  NULL ,
	PhoneNumber int  NULL ,
	Email varchar(60)  NULL 
)
go

ALTER TABLE Employers
	ADD CONSTRAINT Employers_EmployerCode DEFAULT (NEWID()) FOR EmployerCode
go


ALTER TABLE Employers
	ADD CONSTRAINT S4 PRIMARY KEY  CLUSTERED (EmployerCode ASC)
go


CREATE TABLE Positions
(
	PositionCode uniqueidentifier  NOT NULL ,
	Position nvarchar(60)  NOT NULL 
)
go

ALTER TABLE Positions
	ADD CONSTRAINT Positions_PositionCode DEFAULT (NEWID()) FOR PositionCode
go

ALTER TABLE Positions
	ADD CONSTRAINT S5 PRIMARY KEY  CLUSTERED (PositionCode ASC)
go


CREATE TABLE Vacancies
(
	VacancyCode uniqueidentifier  NOT NULL ,
	EmployerCode uniqueidentifier  NOT NULL ,
	PlacementDate datetime  NULL ,
	PositionCode uniqueidentifier  NOT NULL ,
	Salary money  NULL ,
	Schedule nvarchar(60)  NULL ,
	VacancyStatus nvarchar(60)  NOT NULL 
)
go

ALTER TABLE Vacancies
	ADD CONSTRAINT Vacancies_VacancyCode DEFAULT (NEWID()) FOR VacancyCode
go

ALTER TABLE Vacancies
	ADD CONSTRAINT S6 PRIMARY KEY  CLUSTERED (VacancyCode ASC)
go



ALTER TABLE Applicants
	ADD CONSTRAINT  R_5 FOREIGN KEY (PositionCode) REFERENCES Positions(PositionCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go



ALTER TABLE ApplicantData
	ADD CONSTRAINT  R_6 FOREIGN KEY (ApplicantCode) REFERENCES Applicants(ApplicantCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE ApplicantData
	ADD CONSTRAINT  R_8 FOREIGN KEY (EducationCode) REFERENCES EducationData(EducationCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go



ALTER TABLE Vacancies
	ADD CONSTRAINT  R_4 FOREIGN KEY (PositionCode) REFERENCES Positions(PositionCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE Vacancies
	ADD CONSTRAINT  R_9 FOREIGN KEY (EmployerCode) REFERENCES Employers(EmployerCode)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

