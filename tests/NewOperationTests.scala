package shellcuts

import org.scalatest.{
  FlatSpec,
  EitherValues
}
import shellcuts.core.{
  NewOperation,
  Shellcut,
  Configuration
}

class NewOperationTests extends FlatSpec with EitherValues {

  "The New operation" should "add a new shellcut to the configuration" in {
    val originalConfig = Configuration(None, None, List())
    val newConfig = NewOperation.modify(
      originalConfig,
      List(),
      List("gooble", "graeble", "gremmle")
    )
    val expectedShellcut = Shellcut("gooble", Some("graeble"), List("gremmle"))

    assert(newConfig.right.value.shellcuts.head == expectedShellcut)
  }

  /*
  it should "fail" in {
    assert(1 != 1, "big fucked")
  }*/
}
