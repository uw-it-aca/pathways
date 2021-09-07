export function proccessSeaMajors(majors) {
  let majorList = Object.entries(majors['colleges'])
    .flatMap(([college, majors]) => {
      return majors.map(major => {
        major.college = college;
        major.campus = 'Seattle';

        return major;
      });
    });

  return majorList;
}