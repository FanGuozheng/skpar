# Data for auorg
SkdefVersion = 1

Globals {
  XCFunctional = pbe
  Superposition = density
}


AtomParameters {
  Li {
    AtomConfig {
      AtomicNumber = 3
      Mass = 6.941
      Occupations {
        1S = 1.0 1.0
        2S = 1.0 0.0
        2P = 0.0 0.0
      }
      ValenceShells = 2s 2p
      Relativistics = None
    }
    DftbAtom {
      ShellResolved = No
      DensityCompression = PowerCompression { Power = 2; Radius = 11.0 }
      WaveCompressions = SingleAtomCompressions {
        S = PowerCompression { Power = 2; Radius = %(Li_r_s)f }
        P = PowerCompression { Power = 2; Radius = %(Li_r_p)f }
      }
    }
  }
}


OnecenterParameters {

  $StandardDeltaFilling {
    DeltaFilling = 0.01
  }

  Li {
    $StandardDeltaFilling
    Calculator = SlaterAtom {
      Exponents {
        S = 0.50 1.22 3.0
        P = 0.50 1.22 3.0
      }
      MaxPowers {
        S = 3
        P = 3
      }
    }
  }
}

TwoCenterParameters {

  $EqGrid = EquidistantGrid {
      GridStart = 0.4
      GridSeparation = 0.02
      Tolerance = 5e-5
      MaxDistance = 40.0
  }

  # Various specific cutoffs to match SK-file cutoffs in mio-1-1
  $EqGridCutoff10 = EquidistantGrid {
      GridStart = 0.4
      GridSeparation = 0.02
      Tolerance = 5e-5
      MaxDistance = -10.001
  }

  $SkTwocnt_400_200 = Sktwocnt {
    IntegrationPoints = 400 200
  }

  Li-Li { Grid = $EqGridCutoff10; Calculator = $SkTwocnt_400_200 }
}
