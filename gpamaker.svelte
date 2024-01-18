const axios = require('axios'); // axios is a popular HTTP client for JavaScript

async function getCourseGrade() {
    const courseName = prompt("Enter a course: "); // 'prompt' is used in browsers. For Node.js, you'll need a package like 'readline'

    try {
        const response = await axios.get(`https://api.planetterp.com/v1/grades?course=${courseName}`);
        const gradeData = response.data;

        if ('error' in gradeData && gradeData.error === "course not found") {
            throw new Error(`course ${courseName} not found`);
        }

        let count = 0;
        let averageGPA = 0;

        gradeData.forEach(data => {
            if (data.professor === "Clyde Kruskal") {
                const totalPeople = data['A+'] + data['A'] + data['A-'] + data['B+'] + data['B'] + data['B-'] +
                                    data['C+'] + data['C'] + data['C-'] + data['D+'] + data['D'] + data['D-'] + data['F'];

                const totalGPA = data['A+'] * 4.0 + data['A'] * 4.0 + data['A-'] * 3.7 + data['B+'] * 3.3 + data['B'] * 3.0 +
                                 data['B-'] * 2.7 + data['C+'] * 2.3 + data['C'] * 2.0 + data['C-'] * 1.7 + data['D+'] * 1.3 +
                                 data['D'] * 1.0 + data['D-'] * 0.7 + data['F'] * 0.0;

                const totalAverage = totalGPA / totalPeople;
                averageGPA += totalAverage;
                count++;
            }
        });

        if (count > 0) {
            console.log(averageGPA / count);
        } else {
            console.log('No data found for specified professor.');
        }
    } catch (error) {
        console.error(error.message);
    }
}

getCourseGrade();
