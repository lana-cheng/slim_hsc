**Submit a Job**

1. Navigate to the directory containing the file you want to run
2. Grant yourself permission to execute the file using "chmod +x #file_name#". You can use "ls -l" to check for permission. 
3. Use "sbatch #file_name#" to submit the job. The file is the shell script in *bash_code*

"sqme": Check my job
"squeue": Lists all jobs for everyone
"scanel #JobID#": Cancels job
"sacct -j #JobID#": Check the status of a job that's completed

**Check Memory Usage**

If the job is still running: "sstat -j #job_ID#.batch --format=JobID,MaxRSS"

- MaxRSS: Physical RAM used

**Other Command Line Functions**

- "mkdir": Make directory
- Control + Tilda: open new bash window