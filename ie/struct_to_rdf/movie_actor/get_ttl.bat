@echo off&setlocal enabledelayedexpansion

set db=baidu_baike
set file=kg_demo_mapping_%db%.ttl

call generate-mapping -u root -p root -o %file% jdbc:mysql:///%db%?useSSL=false

:: call findstr /i /v /C:"@prefix vocab" "%file%">>%file%.bk
:: move /y %file%.bk %file%

for /f "tokens=1,* delims=:" %%b in ('findstr /n ".*" "%file%"')do (
	set "var=%%c"
	if "!var!" neq "@prefix vocab: <vocab/> ." (
		if "!var!" equ "" (
			>>%file%.bk echo,!var!) ^
		else if "!var!" equ "@prefix jdbc: <http://d2rq.org/terms/jdbc/> ." (
		  >>%file%.bk echo,!var!
			>>%file%.bk echo,@prefix : ^<http://www.kgdemo.com#^> .) ^
		else (
			echo;"!var!"|find "jdbcDSN"&&(
				>>%file%.bk echo,  d2rq:jdbcDSN ^"jdbc:mysql:///%db%?useUnicode=true^&characterEncoding=utf8^&useSSL=false^";)||(
				set "var=!var:vocab= !"
	    	set "var=!var:actor_actor=actor!"
	    	set "var=!var:movie_movie=movie!"
	    	set "var=!var:genre_genre=genre!"
	    	set "var=!var:class  :actor=class  :Actor!"
	    	set "var=!var:class  :movie=class  :Movie!"
	    	set "var=!var:class  :genre=class  :Genre!"
	    	set "var=!var:property  :actor_to_movie=property  :hasActedIn!"
	    	set "var=!var:property  :movie_to_genre=property  :hasGenre!"	    	
	    	>>%file%.bk echo,!var!))
	)
)
move /y %file%.bk %file%