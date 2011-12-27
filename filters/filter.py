#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

class Filter:
    """
        Class to use as a base class for new filters.
    """
    name = "Gaussian blur"
    options = ()

    def __init__(self, title):
        self.title = title
        self.rendering_time = 124121

    def __call__(self, options, cv_image):
        """
            Each filter must returns a new OpenCV image, result of the filter
            application.
        """
        return cv_image

    @property
    def rendering_time_str(self):
        """ Returns a convenient string representation of the rendering time """
        if self.rendering_time == None:
            return None
        elif self.rendering_time > 1000*60:
            return "{0:.2f} min".format(self.rendering_time / 1000. / 60.)
        elif millisec > 1000:
            return "{0:.2f} sec".format(self.rendering_time / 1000.)
        else:
            return "{0} ms".format(self.rendering_time)

    @property
    def options_str(self):
        """ Returns a convenient string representation of the options list """
        if len(self.options) == 0: # No option for this filter
            return "No option"
        else:
            return ", ".join(self.options)

    @property
    def details(self):
        """ Combines the filter's name with the rendering time as a string """
        if self.rendering_time == None: # No rendered yet
            return self.name
        else:
            return "{0} - {1}".format(self.name, self.rendering_time_str)
            
        