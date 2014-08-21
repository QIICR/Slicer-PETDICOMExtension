#include "dcmUnitsConversionHelper.h"
#include <iostream>
#include <cstdlib>
#include <cstring>
//#include "dcmtk/config/osconfig.h"
//#include "dcmtk/dcmdata/dctk.h"
//#include "dcmtk/dcmsr/dsriodcc.h"
//#include "dcmtk/dcmsr/dsrdoc.h"

// ...
// ...............................................................................................
// ...

double ConvertTimeToSeconds(const char *time )
{
  if( time == NULL )
    {
    std::cerr << "ConvertTimeToSeconds got a NULL time string." << std::endl;
    return -1.0;
    }

  std::string h;
  std::string m;
  std::string minAndsecStr;
  std::string secStr;

  double hours;
  double minutes;
  double seconds;

  if( time == NULL )
    {
    return 0.0;
    }

  // ---
  // --- time will be in format HH:MM:SS.SSSS
  // --- convert to a double count of seconds.
  // ---
  std::string timeStr = time;
  //size_t      i = timeStr.find_first_of(":");
  h = timeStr.substr( 0, 2 );
  hours = atof( h.c_str() );

  minAndsecStr = timeStr.substr( 3 );
  //size_t i = minAndsecStr.find_first_of( ":" );
  m = minAndsecStr.substr(0, 2 );
  minutes = atof( m.c_str() );

  secStr = minAndsecStr.substr( 3 );
  seconds = atof( secStr.c_str() );

  double retval = ( seconds
                    + (60.0 * minutes)
                    + (3600.0 * hours ) );
  return retval;
};

// ...
// ...............................................................................................
// ...
double ConvertWeightUnits(double count, const char *fromunits, const char *tounits )
{

  double conversion = count;

  if( fromunits == NULL )
    {
    std::cout << "Got NULL parameter fromunits. A bad param was probably specified." << std::endl;
    return -1.0;
    }
  if( tounits == NULL )
    {
    std::cout << "Got NULL parameter from tounits. A bad parameter was probably specified." << std::endl;
    return -1.0;
    }

  /*
    possibilities include:
  ---------------------------
  "kilograms [kg]"
  "grams [g]"
  "pounds [lb]"
  */

  // --- kg to...
  if( !strcmp(fromunits, "kg") )
    {
    if( !strcmp(tounits, "kg") )
      {
      return conversion;
      }
    else if( !strcmp(tounits, "g") )
      {
      conversion *= 1000.0;
      }
    else if( !strcmp(tounits, "lb") )
      {
      conversion *= 2.2;
      }
    }
  else if( !strcmp(fromunits, "g") )
    {
    if( !strcmp(tounits, "kg") )
      {
      conversion /= 1000.0;
      }
    else if( !strcmp(tounits, "g") )
      {
      return conversion;
      }
    else if( !strcmp(tounits, "lb") )
      {
      conversion *= .0022;
      }
    }
  else if( !strcmp(fromunits, "lb") )
    {
    if( !strcmp(tounits, "kg") )
      {
      conversion *= 0.45454545454545453;
      }
    else if( !strcmp(tounits, "g") )
      {
      conversion *= 454.54545454545453;
      }
    else if( !strcmp(tounits, "lb") )
      {
      return conversion;
      }
    }
  return conversion;

};

// ...
// ...............................................................................................
// ...
double ConvertRadioactivityUnits(double count, const char *fromunits, const char *tounits )
{

  double conversion = count;

  if( fromunits == NULL )
    {
    std::cout << "Got NULL parameter in fromunits. A bad parameter was probably specified." << std::endl;
    return -1.0;
    }
  if( tounits == NULL )
    {
    std::cout << "Got NULL parameter in tounits. A bad parameter was probably specified." << std::endl;
    return -1.0;
    }

/*
  possibilities include:
  ---------------------------
  "megabecquerels [MBq]"
  "kilobecquerels [kBq]"
  "becquerels [Bq]"
  "millibecquerels [mBq]"
  "microbecquerels [uBq]
  "megacuries [MCi]"
  "kilocuries [kCi]"
  "curies [Ci]"
  "millicuries [mCi]"
  "microcuries [uCi]"
*/

  // --- MBq to...
  if( !strcmp(fromunits, "MBq" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 1000000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 1000000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 1000000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.000000000027027027027027;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.000000027027027027027;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.000027027027027027;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.027027027027027;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 27.027027027;
      }
    }
  // --- kBq to...
  else if( !strcmp(fromunits, "kBq" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= .001;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 1000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 1000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.000000000027027027027027;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.000000027027027027027;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.000027027027027027;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 0.027027027027027;
      }
    }
  // --- Bq to...
  else if( !strcmp(fromunits, "Bq" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 0.000001;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 1000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.000000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *=  0.000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.000000000027027027027027;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.000000027027027027027;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 0.000027027027027027;
      }
    }
  // --- mBq to...
  else if( !strcmp(fromunits, "mBq" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 0.000000001;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 0.000001;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.00000000000000000002702702702702;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.000000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.000000000027027027027027;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 0.000000027027027027027;
      }
    }
  // --- uBq to...
  else if( !strcmp(fromunits, "uBq" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 0.000000000001;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 0.000000001;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 0.000001;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.000000000000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.000000000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.000000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.000000000000027027027027027;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 0.000000000027027027027027;
      }
    }
  // --- MCi to...
  else if( !strcmp(fromunits, "MCi" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 37000000000.0;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 37000000000000.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 37000000000000000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 37000000000000000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *=  37000000000000000000848.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 1000000.0;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 1000000000.0;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 1000000000000.0;
      }
    }
  // --- kCi to...
  else if( !strcmp(fromunits, "kCi" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 37000000.0;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 37000000000.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 37000000000000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 37000000000000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 37000000000000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 1000000.0;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 1000000000.0;
      }
    }
  // --- Ci to...
  else if( !strcmp(fromunits, "Ci" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 37000.0;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 37000000.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 37000000000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 37000000000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 37000000000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.0000010;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 1000.0;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 1000000.0;
      }
    }
  // --- mCi to...
  else if( !strcmp(fromunits, "mCi" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 37.0;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 37000.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 37000000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 37000000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 37000000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.0000000010;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.0000010;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      return conversion;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      conversion *= 1000.0;
      }
    }
  // --- uCi to...
  else if( !strcmp(fromunits, " uCi" ) )
    {
    if( !(strcmp(tounits, "MBq" ) ) )
      {
      conversion *= 0.037;
      }
    else if( !(strcmp(tounits, "kBq" ) ) )
      {
      conversion *= 37.0;
      }
    else if( !(strcmp(tounits, "Bq" ) ) )
      {
      conversion *= 37000.0;
      }
    else if( !(strcmp(tounits, "mBq" ) ) )
      {
      conversion *= 37000000.0;
      }
    else if( !(strcmp(tounits, " uBq" ) ) )
      {
      conversion *= 37000000000.0;
      }
    else if( !(strcmp(tounits, "MCi" ) ) )
      {
      conversion *= 0.0000000000010;
      }
    else if( !(strcmp(tounits, "kCi" ) ) )
      {
      conversion *= 0.0000000010;
      }
    else if( !(strcmp(tounits, "Ci" ) ) )
      {
      conversion *= 0.0000010;
      }
    else if( !(strcmp(tounits, "mCi" ) ) )
      {
      conversion *= 0.001;
      }
    else if( !(strcmp(tounits, "uCi" ) ) )
      {
      return conversion;
      }
    }

  return conversion;
};

