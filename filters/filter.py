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
        self.rendering_time = 112

    def __call__(self, options, cv_image):
        """
            Each filter must returns a new OpenCV image, result of the filter
            application.
        """
        return cv_image