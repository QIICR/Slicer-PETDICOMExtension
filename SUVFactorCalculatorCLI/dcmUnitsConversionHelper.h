/*----------------------------------------------------------------------

  Helper functions for converting units in SUVFactorCalculator.cxx

-----------------------------------------------------------------------*/

#ifndef __dcmUnitsConversionHelper_h
#define __dcmUnitsConversionHelper_h

double ConvertTimeToSeconds(const char *time );
double ConvertWeightUnits(double count, const char *fromunits, const char *tounits );
double ConvertRadioactivityUnits(double count, const char *fromunits, const char *tounits );

#endif
