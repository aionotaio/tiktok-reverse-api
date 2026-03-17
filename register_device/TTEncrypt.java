package com.bytedance.frameworks.core.encrypt;

import cn.banny.auxiliary.Inspector;
import cn.banny.unidbg.Module;
import cn.banny.unidbg.arm.ARMEmulator;
import cn.banny.unidbg.linux.android.AndroidARMEmulator;
import cn.banny.unidbg.linux.android.AndroidResolver;
import cn.banny.unidbg.linux.android.dvm.DalvikModule;
import cn.banny.unidbg.linux.android.dvm.DvmClass;
import cn.banny.unidbg.linux.android.dvm.VM;
import cn.banny.unidbg.linux.android.dvm.array.ByteArray;
import cn.banny.unidbg.memory.Memory;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.zip.GZIPOutputStream;

public class TTEncrypt {
   private final ARMEmulator emulator = new AndroidARMEmulator("com.qidian.dldl.official");
   private final VM vm;
   private final Module module;
   private final DvmClass TTEncryptUtils;

   private TTEncrypt() throws IOException {
      Memory memory = this.emulator.getMemory();
      memory.setLibraryResolver(new AndroidResolver(23, new String[0]));
      memory.setCallInitFunction();
      this.vm = this.emulator.createDalvikVM((File)null);
      this.vm.setVerbose(true);
      DalvikModule dm = this.vm.loadLibrary(new File("example_binaries/libttEncrypt.so"), false);
      dm.callJNI_OnLoad(this.emulator);
      this.module = dm.getModule();
      this.TTEncryptUtils = this.vm.resolveClass("com/bytedance/frameworks/core/encrypt/TTEncryptUtils", new DvmClass[0]);
   }

   private void destroy() throws IOException {
      this.emulator.close();
      System.out.println("destroy");
   }

   public static void main(String[] args) throws Exception {
      TTEncrypt test = new TTEncrypt();
      String str = "{\"_gen_time\":\"" + args[0] + "\",\"header\":{\"access\":\"wifi\",\"aid\":1340,\"app_version\":\"42.9.3\",\"appkey\":\"57bfa27c67e58e7d920028d3\",\"build_serial\":\"41488569\",\"carrier\":\"MegaFon\",\"channel\":\"googleplay\",\"clientudid\":\"2c12323d-825a-4bc9-9e3c-25bbceea10b0\",\"cpu_abi\":\"arm64-v8a\",\"density_dpi\":240,\"device_brand\":\"samsung\",\"device_id\":\"\",\"device_manufacturer\":\"samsung\",\"device_model\":\"SM-A805N\",\"display_density\":\"hdpi\",\"display_name\":\"TikTok Lite\",\"language\":\"ru\",\"manifest_version_code\":550,\"mc\":\"" + args[3] + "\",\"mcc_mnc\":\"46000\",\"not_request_sender\":0,\"openudid\":\"" + args[2] + "\",\"os\":\"Android\",\"os_api\":25,\"os_version\":\"7.1.2\",\"packageX\":\"com.ss.android.ugc.aweme\",\"region\":\"RU\",\"release_build\":\"abb8e76_20260306\",\"resolution\":\"1600x900\",\"rom\":\"eng.se.infra.20181117.120021\",\"rom_version\":\"samsung-user 5.1.1 20171130.276299 release-keys\",\"sdk_version\":\"2.5.5.8\",\"serial_number\":\"41488569\",\"sig_hash\":\"aea615ab910015038f73c47e45d21466\",\"sim_region\":\"ru\",\"sim_serial_number\":[{\"sim_serial_number\":\"70459549640190877299\"}],\"timezone\":28800,\"tz_name\":\"Asia\\\\/Shanghai\",\"tz_offset\":0,\"udid\":\"" + args[1] + "\",\"update_version_code\":420903,\"version_code\":420903},\"magic_tag\":\"ss_app_log\"}";
      test.ttEncrypt(str);
      test.destroy();
   }

   private void ttEncrypt(String str) throws IOException {
      long start = System.currentTimeMillis();
      byte[] bArr2 = str.getBytes("UTF-8");
      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(8192);
      GZIPOutputStream gZIPOutputStream = new GZIPOutputStream(byteArrayOutputStream);
      gZIPOutputStream.write(bArr2);
      gZIPOutputStream.close();
      bArr2 = byteArrayOutputStream.toByteArray();
      Number ret = this.TTEncryptUtils.callStaticJniMethod(this.emulator, "ttEncrypt([BI)[B", new Object[]{this.vm.addLocalObject(new ByteArray(bArr2)), bArr2.length});
      long hash = (long)ret.intValue() & 4294967295L;
      ByteArray array = (ByteArray)this.vm.getObject(hash);
      this.vm.deleteLocalRefs();
      Inspector.inspect((byte[])array.getValue(), "ttEncrypt ret=" + ret + ", offset=" + (System.currentTimeMillis() - start) + "ms");
   }
}
