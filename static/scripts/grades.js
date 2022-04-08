const grades = document.getElementsByClassName("grades");
const calcAvg = async (grades) => {
    let avg = 0;
    let retValue = new Promise(function (res,rej) {
        setTimeout(() => {
            for(let i = 0; i < grades.length; i++){
                gradeNum = parseInt(grades[i].innerHTML);
                avg += gradeNum;
            }
            res(avg / grades.length);
        }, 0);
    });
    return retValue;
}



async function getGrade(grades){
    let avg = await calcAvg(grades);
    return avg;
}

let mark = 0;
getGrade(grades).then((res) =>{
    mark = res;
    let gpa = checkGPA(mark).toFixed(1);

    document.getElementById("gpa-container").innerHTML = `GPA: ${gpa}`;
    document.getElementById("average-container").innerHTML = `Average: ${mark}%`;


})

const checkGPA = (grade) => {
    var gpa = 0.0;
    if(grade >= 85 && grade <= 100){
        gpa = 4.0; 
    }
    else if(grade >= 80){
        gpa = 3.7
    }
    else if(grade >= 77){
        gpa = 3.3;
    }
    else if(grade >= 73){
        gpa = 3.0;
    }
    else if(grade >= 70){
        gpa = 2.7;
    }
    else if(grade >= 67){
        gpa = 2.3;
    }
    else if(grade >= 63){
        gpa = 2.0;
    }
    else if(grade >= 60){
        gpa = 1.7;
    }
    else if(grade >= 57){
        gpa = 1.3;
    }
    else if(grade >= 53){
        gpa = 1.0;
    }
    else if(grade >= 50){
        gpa = 0.7
    }
    else{
        gpa = 0.0
    }
    return gpa;
}


