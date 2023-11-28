# TidalEnergy
My code for Technologies for Sustainable Energy final coursework on Tidal Energy
Contents:
  Assignment File:
    TSE Design Exercise Assessment - Student Release - v1.3.pdf   --  Assignment Brief
  Python Files:
    main.py -- reads East and North Component data from CSV files, calculates power and energy output,
      plots flow velocity over different timescales. Q5-8
    powercurve.py -- importable code to handle power curve calculations, fitting Q5-8
    OperationsAndMaintenance.py -- code for Q9.
  .csv Files:
    16M_Powercurve.csv -- cleaned power vs. flow velocity data for 16m rotor
    20M_Powercurve.csv -- cleaned power vs. flow velocity data for 20m rotor
    EastDataCleaned.csv -- cleaned east component velocity data from ADCP, by time and depth cell
    NorthDataCleaned.csv -- cleaned north component velocity data from ADCP, by time and depth cell
    Threasholding.csv -- cleaned data on Hm0, UREF, Power, and Time for O&M activities. Q9 and Q10
