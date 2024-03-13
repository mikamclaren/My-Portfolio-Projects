-- Objectives
-- Come up with flu shots dashboard for 2022 that does the following

-- 1. Total % of patients getting flu shots stratified by
-- 		a. Age (must be 6 mos and older to get flu shot)
-- 		b. Race
-- 		c. County (on a map)
-- 		d. Overall
-- 2. Running Total of flu shots over the course of 2022
-- 3. Total number of flue shots given in 2022
-- 4. A list of patients that show whether or not they received the flu shots

-- Requirements:

-- Patients must have been "Active at our hospital"



-- CODE START


-- create CTE that selects distinct active patients over the last 2 years (2020 start) 
-- that have not died and are >=6 months old as of the end of 2022.

WITH active_patients AS
(
	SELECT distinct patient
	FROM encounters AS e
	JOIN patients AS pat
		ON e.patient = pat.id
	WHERE START BETWEEN '2020-01-01 00:00' and '2022-12-31 23:59'
		AND pat.deathdate IS null
		AND extract(month from age('2022-12-31', pat.birthdate)) >= 6
),


-- create a CTE that selects the earliest date that the patient received a flu shot (code = 5302) in 2022
-- so that patients who may have gotten >1 flu shot are accounted for only a single time.

flu_shot_2022 AS
(
SELECT patient, min(date) as earliest_flu_shot_2022
FROM immunizations
WHERE code = '5302'
	AND date BETWEEN '2022-01-01 00:00' AND '2022-12-31 23:59'
GROUP BY patient
)

-- Select the data that you want displayed from the patients (pat) table along with a left join on patient id 
-- from flu_shot_2022 (abbreviated as flu). Add a binary (1,0) when the patient column is not null, meaning they 
-- got a flu shot (1) or is null, meaning they didn't get one (0) and name the binary column 'flu_shot_2022'.
-- Then ensure the patients are active by encorporating the query for active patients, further filtering pts out.

SELECT pat.birthdate,
	pat.race,
	pat.county,
	pat.id,
	pat.first,
	pat.last,
	pat.gender,
	extract(YEAR from age('12-31-2022', birthdate)) as age,
	flu.earliest_flu_shot_2022,
	flu.patient,
	CASE WHEN flu.patient is not null then 1
	ELSE 0
	END AS flu_shot_2022 
FROM patients AS pat
LEFT JOIN flu_shot_2022 AS flu
	ON pat.id = flu.patient
WHERE 1=1
	AND pat.id in (SELECT patient FROM active_patients)
	
-- The resulting data was downloaded and then uploaded on Tableau Public. 
-- Find the visualization here: https://public.tableau.com/app/profile/shemeika.mika.mclaren/viz/FluImmunizationDashboard_17102813893160/Dashboard1
	