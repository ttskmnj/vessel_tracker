# How to set up Metabase on docker container

### 1. open `0.0.0.0:3000` in browser.
Make sure all containers are up. Maybe it will take a few minutes for Metabase container to finish booting.
click `let's get started` to Metabase set up. 

![image](./readme_img/step1.png)

### 2. choose your preferd language

![image](./readme_img/step2.png)

### 3. fill admin data
fill `First name`, `Last name`, `Email`, `Company or team name` and `password`

![image](./readme_img/step3.png)

### 4. database setting
click `Show more options`

![image](./readme_img/step4.png)

choose `MongoDB`

![image](./readme_img/step5.png)
 
fill MongoDB criteria. Please make sure you use MongoDB container name `mongo` as Host and `27017` as Port. then click `connect database`.

![image](./readme_img/step6.png)

### 5. finish Metabase set up
click `finish`

![image](./readme_img/step7.png)

then click `take me to Metabase` to open Metabase dashboard

![image](./readme_img/step8.png)


Now Metabase set up is done!