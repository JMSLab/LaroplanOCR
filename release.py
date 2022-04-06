import os
import time
import shutil

def main():
    
    log_file = open("release.log", 'w')
    log_file.write("Started at " + time.strftime('%I:%M:%S%p %Z on %b %d, %Y\n\n'))
    
    # Compile codebook.md    
    log_file.write(time.strftime('%I:%M:%S%p') + "   : Compilation of codebook.md started\n")
    
    if os.path.exists("codebook.md"):
        os.remove("codebook.md")
    
    os.system('''Rscript -e "rmarkdown::render('codebook.Rmd')"''')
    shutil.copy(src = "codebook.md",
                dst = os.path.join("release", "codebook.md"))
    
    # Make zip file
    log_file.write(time.strftime('%I:%M:%S%p') + "   : Build of release.zip started\n")
    
    if os.path.exists("release"):
        shutil.rmtree("release")
    if os.path.exists("release.zip"):
        os.remove("release.zip")
    
    os.mkdir("release")
    for ff in [os.path.join('raw', 'orig'), 'example']:
        shutil.copytree(src = ff, 
                        dst = os.path.join("release", ff))
    
    shutil.copytree(src = os.path.join("analysis", "output"),
                    dst = os.path.join("release", "datasets"))
    
    shutil.make_archive("release", "zip", "release")
    
    shutil.rmtree("release")
    
    log_file.write("\nFinished at " + time.strftime('%I:%M:%S%p %Z on %b %d, %Y\n'))
    log_file.close()



if __name__ == '__main__':
    main()
