# Each file in this package is named after a specific metric, with the term
# "metric" defined the same way it is in the reports delivered to management
# (i.e. the file reads.py corresponds to "Article Reads" in the reports).
#
# Each file contains all the information needed to execute the Google Analytics
# query for the metric the file is named after. These attributes are organized
# into three classes:  GAQueryBase, GAQueryDefinition, and GAQueryContainer.
#
# The term 'metric' is easily confused with other concepts (especially because
# it is also the name of a datatype built into Google Analytics). Previous
# versions of this code contained a MetricDefinition class, which was intended
# to distinguish the Google Analytics-specific attributes of GAQueryDefinition
# from attributes of the metrics seen in the reports, but the developer decided
# that the class added more confusion than it removed.
#
# Due to (1) the challenges involved in updating the code to meet changes in
# business requirements (i.e. the multiple query versions seen in reads.py),
# (2) the wide variation in complexity between one metric and another,
# and (3) the immense complexity of Google Analytics query filters
# (see googleanalytics/filter_strings.py), it's very difficult to find a
# simple architecture to represent the concept of a "metric definition".
# Each metric is given a separate file in this package because the developer
# believes this is the most maintainable way to scale the code over time to meet
# future reporting requirements.
