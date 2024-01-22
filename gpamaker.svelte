const readline = require('readline');
const axios = require('axios');

async function getCourseGrade() {
        rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question('Enter a course: ', (courseName) => {
        rl.question('Enter a professor: ', async (professorName) => {
            try {
                const response = await axios.get(`https://api.planetterp.com/v1/grades?course=${courseName}`);
                const gradeData = response.data;

                if ('error' in gradeData && gradeData.error === "course not found") {
                    throw new Error(`course ${courseName} not found`);
                }

                let count = 0;
                let averageGPA = 0;

                gradeData.forEach(data => {
                    if (data.professor === professorName) {
                        const totalPeople = data['A+'] + data['A'] + data['A-'] + data['B+'] + data['B'] + data['B-'] +
                                            data['C+'] + data['C'] + data['C-'] + data['D+'] + data['D'] + data['D-'] + data['F'];

                        const totalGPA = data['A+'] * 4.0 + data['A'] * 4.0 + data['A-'] * 3.7 + data['B+'] * 3.3 + data['B'] * 3.0 +
                                         data['B-'] * 2.7 + data['C+'] * 2.3 + data['C'] * 2.0 + data['C-'] * 1.7 + data['D+'] * 1.3 +
                                         data['D'] * 1.0 + data['D-'] * 0.7 + data['F'] * 0.0;

                        if (totalPeople > 0) {
                            const totalAverage = totalGPA / totalPeople;
                            averageGPA += totalAverage;
                            count++;
                        }
                    }
                });

                if (count > 0) {
                    console.log(`Average GPA for Professor ${professorName}: ${(averageGPA / count).toFixed(2)}`);
                } else {
                    console.log(`No data found for Professor ${professorName}.`);
                }
            } catch (error) {
                console.error(error.message);
            } finally {
                rl.close();
            }
        });
    });
}

getCourseGrade();
