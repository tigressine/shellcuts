package shellcuts.core

import org.scalatest.FlatSpec
import shellcuts.core.operations.{
  DeleteOperation,
  GoOperation,
  HelpOperation,
  NewOperation
}

class ParsingSpec extends FlatSpec {
  val parse = Parsing.parse(
    HelpOperation,
    GoOperation,
    HelpOperation,
    Map("-n" -> NewOperation, "-d" -> DeleteOperation)
  ) _

  "parse()" should "process zero arguments" in {
    val givenArguments = Array[String]()
    val expectedOperation = HelpOperation
    val expectedParameters = List[String]()

    val (parsedOperation, parsedParameters) = parse(givenArguments)
    assert(expectedOperation == parsedOperation)
    assert(expectedParameters == parsedParameters)
  }

  it should "handle an invalid flag" in {
    val givenArguments = Array("--invalid")
    val expectedOperation = HelpOperation
    val expectedParameters = List("--invalid")

    val (parsedOperation, parsedParameters) = parse(givenArguments)
    assert(expectedOperation == parsedOperation)
    assert(expectedParameters == parsedParameters)
  }

  it should "process a valid flag" in {
    val givenArguments = Array("-n")
    val expectedOperation = NewOperation
    val expectedParameters = List[String]()

    val (parsedOperation, parsedParameters) = parse(givenArguments)
    assert(expectedOperation == parsedOperation)
    assert(expectedParameters == parsedParameters)
  }

  it should "process a valid flag with additional parameters" in {
    val givenArguments = Array("-n", "name", "follow")
    val expectedOperation = NewOperation
    val expectedParameters = List("name", "follow")

    val (parsedOperation, parsedParameters) = parse(givenArguments)
    assert(expectedOperation == parsedOperation)
    assert(expectedParameters == parsedParameters)
  }

  it should "process a shellcut name" in {
    val givenArguments = Array("name")
    val expectedOperation = GoOperation
    val expectedParameters = List("name")

    val (parsedOperation, parsedParameters) = parse(givenArguments)
    assert(expectedOperation == parsedOperation)
    assert(expectedParameters == parsedParameters)
  }
}
