scalaVersion := "2.11.12"
nativeLinkStubs := true
scalaSource in Compile := baseDirectory.value / "source"
scalaSource in Test := baseDirectory.value / "specs"

enablePlugins(ScalaNativePlugin)

libraryDependencies ++= Seq(
  "org.scalatest" % "scalatest_native0.3_2.11" % "3.2.0-SNAP10"
)
