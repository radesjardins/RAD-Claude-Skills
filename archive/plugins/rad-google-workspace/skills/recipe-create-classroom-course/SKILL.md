---
name: recipe-create-classroom-course
version: 1.0.0
description: "This skill should be used when the user says \"set up a new classroom course\", \"create a class in Google Classroom\", \"add students to my course\", \"start a new course\", \"invite students to Classroom\", or wants to create a Google Classroom course and enroll students via invitations."
metadata:
  openclaw:
    category: "recipe"
    domain: "education"
    requires:
      bins: ["gws"]
      skills: ["gws-classroom"]
---

# Create a Google Classroom Course

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-classroom`

Create a Google Classroom course and invite students.

## Steps

1. Create the course: `gws classroom courses create --json '{"name": "Introduction to CS", "section": "Period 1", "room": "Room 101", "ownerId": "me"}'`
2. Invite a student: `gws classroom invitations create --json '{"courseId": "COURSE_ID", "userId": "student@school.edu", "role": "STUDENT"}'`
3. List enrolled students: `gws classroom courses students list --params '{"courseId": "COURSE_ID"}' --format table`

