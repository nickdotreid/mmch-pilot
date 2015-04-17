var gulp = require('gulp'), 
	addsrc = require('gulp-add-src')
    sass = require('gulp-ruby-sass') 
    notify = require("gulp-notify") 
    concat = require('gulp-concat')
    uglify = require('gulp-uglify'),
    bower = require('gulp-bower');

var config = {
     sassPath: './resources/sass',
     bowerDir: './bower_components' 
}

gulp.task('bower', function() { 
    return bower()
         .pipe(gulp.dest(config.bowerDir)) 
});

gulp.task('icons', function() { 
    return gulp.src(config.bowerDir + '/fontawesome/fonts/**.*') 
        .pipe(gulp.dest('./mmch_pilot/static/fonts')); 
});

gulp.task('css', function() { 
    return sass(config.sassPath + '/styles.scss', {
             style: 'compressed',
             loadPath: [
                 './resources/sass',
                 config.bowerDir + '/bootstrap-sass-official/assets/stylesheets',
                 config.bowerDir + '/fontawesome/scss',
             ]
         }) 
         .pipe(gulp.dest('./mmch_pilot/static/css')); 
});

gulp.task('js', function(){
	gulp.src('')
		.pipe(addsrc(config.bowerDir+'/jquery/dist/jquery.min.js'))
		.pipe(addsrc(config.bowerDir + '/bootstrap-sass-official/assets/javascripts/bootstrap/tab.js'))
		.pipe(uglify())
		.pipe(concat("vendor.min.js"))
		.pipe(gulp.dest('./mmch_pilot/static/js'));
});

// Rerun the task when a file changes
 gulp.task('watch', function() {
     gulp.watch(config.sassPath + '/**/*.scss', ['css']); 
});

  gulp.task('default', ['bower', 'icons', 'css', 'js']);