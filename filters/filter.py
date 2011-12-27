#!/usr/bin/env python2

# Raphael Javaux <raphaeljavaux@gmail.com> - December 2011

class Filter:
    """
        Class to use as a base class for new filters.
    """
    name = "Gaussian blur"
    properties = ()

    def __init__(self, title):
        self.title = title

    def __call__(self, properties, cv_image):
        """
            Each filter must returns a new OpenCV image, result of the filter
            application.
        """
        return cv_image